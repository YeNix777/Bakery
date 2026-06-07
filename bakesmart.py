from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).parent / "archive" / "Bakery sales.csv"
PRODUCT_COUNT = 3


@dataclass(frozen=True)
class ForecastResult:
    product: str
    weekday: str
    predicted_demand: float
    recommended_production: int
    expected_sales: float
    expected_waste: float
    expected_lost_sales: float
    selling_price: float
    production_cost: float
    estimated_revenue: float
    estimated_profit: float


def parse_price(price: object) -> float:
    """Convert values such as '1,20 €' into 1.20."""
    cleaned = (
        str(price)
        .replace("€", "")
        .replace("\u00a0", "")
        .replace(",", ".")
        .strip()
    )
    return float(cleaned)


def load_sales(path: Path = DATA_PATH) -> pd.DataFrame:
    sales = pd.read_csv(path, usecols=["date", "article", "Quantity", "unit_price"])
    sales["date"] = pd.to_datetime(sales["date"], errors="coerce")
    sales["Quantity"] = pd.to_numeric(sales["Quantity"], errors="coerce")
    sales["unit_price_eur"] = sales["unit_price"].map(parse_price)
    sales = sales.dropna(subset=["date", "article", "Quantity", "unit_price_eur"])
    sales = sales[sales["Quantity"] > 0].copy()
    sales["article"] = sales["article"].astype(str).str.strip()
    return sales


def get_top_products(sales: pd.DataFrame, count: int = PRODUCT_COUNT) -> list[str]:
    return (
        sales.groupby("article")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(count)
        .index.tolist()
    )


def build_daily_sales(sales: pd.DataFrame, products: list[str]) -> pd.DataFrame:
    selected = sales[sales["article"].isin(products)]
    daily = (
        selected.groupby(["date", "article"], as_index=False)["Quantity"]
        .sum()
        .rename(columns={"article": "product", "Quantity": "units_sold"})
    )

    # Use observed trading dates only. Missing dates may be days when the bakery
    # was closed and should not automatically count as zero demand.
    all_dates = pd.DatetimeIndex(sorted(sales["date"].unique()))
    full_index = pd.MultiIndex.from_product(
        [all_dates, products], names=["date", "product"]
    )
    daily = (
        daily.set_index(["date", "product"])
        .reindex(full_index, fill_value=0)
        .reset_index()
    )
    daily["weekday_number"] = daily["date"].dt.weekday
    daily["weekday"] = daily["date"].dt.day_name()
    return daily


def typical_price(sales: pd.DataFrame, product: str) -> float:
    product_sales = sales[sales["article"] == product]
    if product_sales.empty:
        raise ValueError(f"No sales found for {product}.")
    return float(product_sales["unit_price_eur"].median())


def weekday_average(
    daily_sales: pd.DataFrame, product: str, weekday_number: int
) -> float:
    matching_days = daily_sales[
        (daily_sales["product"] == product)
        & (daily_sales["weekday_number"] == weekday_number)
    ]
    if matching_days.empty:
        raise ValueError("No historical observations match this selection.")
    return float(matching_days["units_sold"].mean())


def create_forecast(
    daily_sales: pd.DataFrame,
    product: str,
    forecast_date: pd.Timestamp,
    selling_price: float,
    cost_ratio: float = 0.45,
    safety_buffer: float = 0.05,
) -> ForecastResult:
    predicted = weekday_average(daily_sales, product, forecast_date.weekday())
    recommended = max(0, round(predicted * (1 + safety_buffer)))
    expected_sales = min(float(recommended), predicted)
    expected_waste = max(float(recommended) - predicted, 0.0)
    expected_lost_sales = max(predicted - float(recommended), 0.0)
    production_cost = selling_price * cost_ratio
    revenue = expected_sales * selling_price
    profit = revenue - recommended * production_cost

    return ForecastResult(
        product=product,
        weekday=forecast_date.day_name(),
        predicted_demand=predicted,
        recommended_production=recommended,
        expected_sales=expected_sales,
        expected_waste=expected_waste,
        expected_lost_sales=expected_lost_sales,
        selling_price=selling_price,
        production_cost=production_cost,
        estimated_revenue=revenue,
        estimated_profit=profit,
    )


def simulate_strategy(
    daily_sales: pd.DataFrame,
    product: str,
    selling_price: float,
    cost_ratio: float,
    safety_buffer: float,
) -> pd.DataFrame:
    product_daily = daily_sales[daily_sales["product"] == product].copy()
    weekday_means = product_daily.groupby("weekday_number")["units_sold"].mean()
    product_daily["predicted_demand"] = product_daily["weekday_number"].map(
        weekday_means
    )
    product_daily["recommended_production"] = (
        product_daily["predicted_demand"] * (1 + safety_buffer)
    ).round()
    product_daily["estimated_waste"] = (
        product_daily["recommended_production"] - product_daily["units_sold"]
    ).clip(lower=0)
    product_daily["lost_sales"] = (
        product_daily["units_sold"] - product_daily["recommended_production"]
    ).clip(lower=0)
    product_daily["estimated_sales"] = product_daily[
        ["recommended_production", "units_sold"]
    ].min(axis=1)
    product_daily["estimated_profit"] = (
        product_daily["estimated_sales"] * selling_price
        - product_daily["recommended_production"] * selling_price * cost_ratio
    )
    return product_daily


def simulate_fixed_strategy(
    daily_sales: pd.DataFrame,
    product: str,
    selling_price: float,
    cost_ratio: float,
    safety_buffer: float,
) -> pd.DataFrame:
    """Simulate producing the same quantity on every observed trading day."""
    product_daily = daily_sales[daily_sales["product"] == product].copy()
    fixed_demand = float(product_daily["units_sold"].mean())
    fixed_production = round(fixed_demand * (1 + safety_buffer))
    product_daily["predicted_demand"] = fixed_demand
    product_daily["recommended_production"] = fixed_production
    product_daily["estimated_waste"] = (
        fixed_production - product_daily["units_sold"]
    ).clip(lower=0)
    product_daily["lost_sales"] = (
        product_daily["units_sold"] - fixed_production
    ).clip(lower=0)
    product_daily["estimated_sales"] = product_daily["units_sold"].clip(
        upper=fixed_production
    )
    product_daily["estimated_profit"] = (
        product_daily["estimated_sales"] * selling_price
        - fixed_production * selling_price * cost_ratio
    )
    return product_daily
