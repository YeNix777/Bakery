from datetime import date, timedelta
import importlib

import pandas as pd
import streamlit as st

import bakesmart


# Streamlit reruns app.py in the same process. Reload the local logic module so
# newly added functions are immediately available during development.
importlib.reload(bakesmart)

DATA_PATH = bakesmart.DATA_PATH
build_daily_sales = bakesmart.build_daily_sales
create_forecast = bakesmart.create_forecast
get_top_products = bakesmart.get_top_products
load_sales = bakesmart.load_sales
simulate_fixed_strategy = bakesmart.simulate_fixed_strategy
simulate_strategy = bakesmart.simulate_strategy
typical_price = bakesmart.typical_price


st.set_page_config(
    page_title="BakeSmart",
    page_icon="BS",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #1f2933;
        --muted: #667085;
        --brand: #9a5b2e;
        --green: #237a57;
        --caramel: #c58b3a;
        --sage: #4f8068;
        --slate-blue: #55758a;
    }
    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(220, 186, 145, 0.16), transparent 28%),
            #f8f9fb;
    }
    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: var(--ink);
        letter-spacing: -0.02em;
    }
    p, .stCaption {
        color: var(--muted);
    }
    [data-testid="stSidebar"] {
        background: #202a34;
        border-right: 0;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] *,
    [data-testid="stSidebar"] input {
        color: var(--ink) !important;
    }
    .hero {
        background: linear-gradient(120deg, #252f39 0%, #3e4b57 68%, #8a5b36 130%);
        border-radius: 20px;
        padding: 34px 38px;
        margin-bottom: 26px;
        box-shadow: 0 14px 35px rgba(31, 41, 51, 0.14);
    }
    .hero-kicker {
        color: #e8c79f;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .hero-title {
        color: #ffffff;
        font-size: 2.45rem;
        font-weight: 750;
        line-height: 1.08;
        margin: 0 0 10px 0;
    }
    .hero-copy {
        color: #e5e9ed;
        font-size: 1.03rem;
        line-height: 1.55;
        max-width: 760px;
        margin: 0;
    }
    .hero-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
        margin-top: 20px;
    }
    .hero-chip {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: #f7eee5;
        background: rgba(255, 255, 255, 0.09);
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 650;
        padding: 7px 11px;
    }
    .hero-chip svg {
        width: 15px;
        height: 15px;
        stroke: #e8c79f;
    }
    .section-kicker {
        color: var(--brand);
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .decision-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        background: #edf8f2;
        border: 1px solid #cce8d9;
        border-left: 6px solid var(--green);
        border-radius: 14px;
        padding: 20px 24px;
        margin: 10px 0 20px 0;
    }
    .decision-label {
        color: #416454;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .decision-main {
        color: #153f2e;
        font-size: 1.35rem;
        font-weight: 750;
        line-height: 1.3;
    }
    .decision-detail {
        color: #527061;
        font-size: 0.92rem;
        margin-top: 4px;
    }
    .method-badge {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        color: #315d49;
        background: #dcefe5;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        padding: 7px 12px;
        white-space: nowrap;
    }
    .method-badge svg {
        width: 16px;
        height: 16px;
        stroke: #315d49;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 4px 0 12px 0;
    }
    .kpi-grid.three {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .kpi-card {
        --accent: var(--brand);
        --tint: #f8eee6;
        background: #ffffff;
        border: 1px solid #e4e7ec;
        border-top: 4px solid var(--accent);
        border-radius: 14px;
        padding: 17px 18px 16px;
        box-shadow: 0 5px 16px rgba(31, 41, 51, 0.06);
    }
    .kpi-card.caramel { --accent: var(--caramel); --tint: #fbf1df; }
    .kpi-card.sage { --accent: var(--sage); --tint: #eaf3ee; }
    .kpi-card.blue { --accent: var(--slate-blue); --tint: #eaf0f4; }
    .kpi-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 13px;
    }
    .kpi-label {
        color: #667085;
        font-size: 0.79rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .kpi-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        background: var(--tint);
        border-radius: 10px;
    }
    .kpi-icon svg {
        width: 18px;
        height: 18px;
        stroke: var(--accent);
    }
    .kpi-value {
        color: var(--ink);
        font-size: 1.62rem;
        font-weight: 760;
        line-height: 1.15;
    }
    .kpi-note {
        color: #7b8490;
        font-size: 0.74rem;
        margin-top: 6px;
    }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e4e7ec;
        border-radius: 14px;
        padding: 17px 18px;
        box-shadow: 0 4px 14px rgba(31, 41, 51, 0.055);
    }
    [data-testid="stMetric"] label,
    [data-testid="stMetric"] [data-testid="stMetricLabel"],
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: var(--ink) !important;
    }
    [data-testid="stMetric"] svg {
        fill: var(--ink) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.82rem;
        font-weight: 650;
    }
    [data-testid="stMetricValue"] {
        font-weight: 750;
    }
    [data-testid="stTabs"] {
        margin-top: 20px;
    }
    [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 1px solid #e4e7ec;
    }
    [data-baseweb="tab"] {
        font-weight: 650;
        padding-left: 4px;
        padding-right: 4px;
    }
    hr {
        border-color: #e4e7ec;
    }
    @media (max-width: 700px) {
        .hero { padding: 26px 24px; }
        .hero-title { font-size: 2rem; }
        .decision-card { align-items: flex-start; flex-direction: column; }
        .kpi-grid, .kpi-grid.three { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 480px) {
        .kpi-grid, .kpi-grid.three { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


ICONS = {
    "chart": (
        '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M3 3v18h18"/><path d="m7 16 4-5 4 3 5-7"/></svg>'
    ),
    "basket": (
        '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<path d="m5 11 4-7"/><path d="m19 11-4-7"/>'
        '<path d="M3 11h18l-2 9H5z"/><path d="M9 15v2"/><path d="M15 15v2"/></svg>'
    ),
    "leaf": (
        '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 18 2 18 2c1 5.5-1 10-5 12"/>'
        '<path d="M2 21c0-3 1.85-5.36 5.08-6.94C9.46 12.9 12.6 12 17 12"/></svg>'
    ),
    "coins": (
        '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v4c0 1.7 3.1 3 7 3s7-1.3 7-3V6"/>'
        '<path d="M5 10v4c0 1.7 3.1 3 7 3s7-1.3 7-3v-4"/>'
        '<path d="M5 14v4c0 1.7 3.1 3 7 3s7-1.3 7-3v-4"/></svg>'
    ),
    "calendar": (
        '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="5" width="18" height="16" rx="2"/>'
        '<path d="M16 3v4M8 3v4M3 10h18"/></svg>'
    ),
    "database": (
        '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<ellipse cx="12" cy="5" rx="8" ry="3"/>'
        '<path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/>'
        '<path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>'
    ),
    "target": (
        '<svg viewBox="0 0 24 24" fill="none" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/>'
        '<circle cx="12" cy="12" r="1"/></svg>'
    ),
}


def kpi_card(label, value, note, icon, color_class=""):
    return (
        f'<div class="kpi-card {color_class}">'
        f'<div class="kpi-top">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-icon">{ICONS[icon]}</div>'
        f"</div>"
        f'<div class="kpi-value">{value}</div>'
        f'<div class="kpi-note">{note}</div>'
        f"</div>"
    )


@st.cache_data
def prepare_data():
    sales = load_sales(DATA_PATH)
    products = get_top_products(sales)
    daily = build_daily_sales(sales, products)
    return sales, products, daily


try:
    sales, products, daily_sales = prepare_data()
except FileNotFoundError:
    st.error(
        "The bakery CSV was not found. Put it at "
        "`archive/Bakery sales.csv` and restart the app."
    )
    st.stop()
except Exception as exc:
    st.error(f"The dataset could not be loaded: {exc}")
    st.stop()


st.markdown(
    f"""
    <div class="hero">
        <div class="hero-kicker">Production intelligence for independent bakeries</div>
        <div class="hero-title">BakeSmart</div>
        <p class="hero-copy">
            Turn historical sales into practical production decisions.
            Forecast demand, reduce unnecessary surplus, and understand the
            financial effect before the first batch goes into the oven.
        </p>
        <div class="hero-chips">
            <span class="hero-chip">{ICONS['database']} 232k+ sales records</span>
            <span class="hero-chip">{ICONS['calendar']} Weekday forecasting</span>
            <span class="hero-chip">{ICONS['leaf']} Waste-aware planning</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## BakeSmart")
    st.caption("Decision settings")
    st.divider()
    st.markdown("### Production plan")
    product = st.selectbox(
        "Product",
        products,
        format_func=lambda value: value.title(),
    )
    forecast_date = st.date_input(
        "Forecast date",
        value=date.today() + timedelta(days=1),
    )
    safety_buffer_percent = st.slider(
        "Safety buffer",
        min_value=0,
        max_value=20,
        value=5,
        help="Extra units prepared to reduce the chance of selling out.",
    )
    cost_percent = st.slider(
        "Production cost (% of selling price)",
        min_value=20,
        max_value=80,
        value=45,
        help="A business assumption because production costs are not in the dataset.",
    )
    st.divider()
    st.caption(
        "Forecast method: historical average for the selected weekday. "
        "Waste and profit are simulated."
    )

price = typical_price(sales, product)
result = create_forecast(
    daily_sales=daily_sales,
    product=product,
    forecast_date=pd.Timestamp(forecast_date),
    selling_price=price,
    cost_ratio=cost_percent / 100,
    safety_buffer=safety_buffer_percent / 100,
)

st.markdown(
    '<div class="section-kicker">Tomorrow\'s production decision</div>',
    unsafe_allow_html=True,
)
st.markdown(f"## {result.weekday}, {forecast_date:%d %B %Y}")
st.markdown(
    f"""
    <div class="decision-card">
        <div>
            <div class="decision-label">Recommended action</div>
            <div class="decision-main">
                Prepare {result.recommended_production} {product.title()} units
            </div>
            <div class="decision-detail">
                Historical {result.weekday} demand averages
                {result.predicted_demand:.1f} units. The recommendation includes
                a {safety_buffer_percent}% safety buffer.
            </div>
        </div>
        <div class="method-badge">{ICONS['target']} Weekday forecast</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="kpi-grid">'
    + kpi_card(
        "Predicted demand",
        f"{result.predicted_demand:.1f} units",
        f"Average historical {result.weekday}",
        "chart",
        "blue",
    )
    + kpi_card(
        "Recommended production",
        f"{result.recommended_production} units",
        f"Includes {safety_buffer_percent}% buffer",
        "basket",
        "caramel",
    )
    + kpi_card(
        "Expected surplus",
        f"{result.expected_waste:.1f} units",
        "Estimated unsold production",
        "leaf",
        "sage",
    )
    + kpi_card(
        "Estimated profit",
        f"EUR {result.estimated_profit:,.2f}",
        "Revenue less production cost",
        "coins",
    )
    + "</div>",
    unsafe_allow_html=True,
)

st.caption(
    f"Typical selling price: EUR {result.selling_price:.2f} per unit | "
    f"Assumed production cost: EUR {result.production_cost:.2f} per unit"
)

chart_tab, impact_tab, portfolio_tab, method_tab = st.tabs(
    ["Demand analysis", "Business simulation", "Product portfolio", "Methodology"]
)

with chart_tab:
    st.markdown(
        '<div class="section-kicker">Demand evidence</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"### Historical daily sales: {product.title()}")
    st.caption(
        "Daily unit sales across the full dataset. Peaks and dips show why a "
        "single fixed production quantity can be inefficient."
    )
    product_history = daily_sales[daily_sales["product"] == product].set_index("date")

    busiest_weekday = (
        product_history.groupby("weekday")["units_sold"].mean().sort_values().index[-1]
    )
    peak_date = product_history["units_sold"].idxmax()
    peak_units = product_history["units_sold"].max()
    average_units = product_history["units_sold"].mean()
    variation = (
        product_history["units_sold"].std() / average_units * 100
        if average_units
        else 0
    )
    st.markdown(
        '<div class="kpi-grid three">'
        + kpi_card(
            "Strongest weekday",
            busiest_weekday,
            "Highest average unit sales",
            "calendar",
            "caramel",
        )
        + kpi_card(
            "Peak sales day",
            f"{peak_units:,.0f} units",
            f"Recorded on {peak_date:%d %b %Y}",
            "chart",
            "blue",
        )
        + kpi_card(
            "Demand variability",
            f"{variation:.0f}%",
            "Higher means demand is less predictable",
            "target",
            "sage",
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    st.line_chart(product_history["units_sold"], color="#c46d26")

    weekday_chart = (
        product_history.groupby(["weekday_number", "weekday"])["units_sold"]
        .mean()
        .reset_index()
        .sort_values("weekday_number")
        .set_index("weekday")[["units_sold"]]
        .rename(columns={"units_sold": "Average units"})
    )
    st.markdown("### Typical weekly demand pattern")
    st.bar_chart(weekday_chart, color="#9a5b2e")

    monthly_demand = (
        product_history["units_sold"]
        .resample("ME")
        .mean()
        .to_frame("Average daily units")
    )
    recent_average = monthly_demand["Average daily units"].tail(3).mean()
    earlier_average = monthly_demand["Average daily units"].head(3).mean()
    trend_change = (
        (recent_average - earlier_average) / earlier_average * 100
        if earlier_average
        else 0
    )
    trend_word = "higher" if trend_change >= 0 else "lower"
    st.markdown("### Monthly demand trend")
    st.caption(
        f"Average daily demand in the final three months was "
        f"{abs(trend_change):.1f}% {trend_word} than in the first three months."
    )
    st.line_chart(monthly_demand, color="#55758a")

with impact_tab:
    simulation = simulate_strategy(
        daily_sales=daily_sales,
        product=product,
        selling_price=price,
        cost_ratio=cost_percent / 100,
        safety_buffer=safety_buffer_percent / 100,
    )
    total_waste = simulation["estimated_waste"].sum()
    total_lost_sales = simulation["lost_sales"].sum()
    total_profit = simulation["estimated_profit"].sum()
    fixed_simulation = simulate_fixed_strategy(
        daily_sales=daily_sales,
        product=product,
        selling_price=price,
        cost_ratio=cost_percent / 100,
        safety_buffer=safety_buffer_percent / 100,
    )
    fixed_waste = fixed_simulation["estimated_waste"].sum()
    fixed_lost_sales = fixed_simulation["lost_sales"].sum()
    fixed_profit = fixed_simulation["estimated_profit"].sum()
    waste_change = (
        (fixed_waste - total_waste) / fixed_waste * 100 if fixed_waste else 0
    )
    lost_sales_change = (
        (fixed_lost_sales - total_lost_sales) / fixed_lost_sales * 100
        if fixed_lost_sales
        else 0
    )
    profit_change = total_profit - fixed_profit

    st.markdown(
        '<div class="section-kicker">Historical scenario</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### What if BakeSmart had planned every recorded day?")
    st.write(
        "This simulation applies the selected weekday strategy to each historical "
        "day and compares recommended production with recorded sales."
    )
    st.markdown(
        '<div class="kpi-grid three">'
        + kpi_card(
            "Simulated unsold units",
            f"{total_waste:,.0f}",
            "Historical scenario estimate",
            "leaf",
            "sage",
        )
        + kpi_card(
            "Simulated missed demand",
            f"{total_lost_sales:,.0f}",
            "Demand above planned production",
            "chart",
            "blue",
        )
        + kpi_card(
            "Simulated total profit",
            f"EUR {total_profit:,.0f}",
            "Across all recorded days",
            "coins",
            "caramel",
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("### BakeSmart versus a fixed daily plan")
    comparison = pd.DataFrame(
        {
            "Strategy": ["Fixed quantity", "BakeSmart weekday plan"],
            "Unsold units": [fixed_waste, total_waste],
            "Missed demand": [fixed_lost_sales, total_lost_sales],
            "Estimated profit (EUR)": [fixed_profit, total_profit],
        }
    ).set_index("Strategy")
    st.dataframe(
        comparison.style.format(
            {
                "Unsold units": "{:,.0f}",
                "Missed demand": "{:,.0f}",
                "Estimated profit (EUR)": "{:,.0f}",
            }
        ),
        width="stretch",
    )

    insight_columns = st.columns(3)
    insight_columns[0].metric(
        "Surplus reduction",
        f"{waste_change:+.1f}%",
        help="Positive means BakeSmart produced fewer unsold units.",
    )
    insight_columns[1].metric(
        "Missed-demand reduction",
        f"{lost_sales_change:+.1f}%",
        help="Positive means BakeSmart missed fewer potential sales.",
    )
    insight_columns[2].metric(
        "Profit difference",
        f"EUR {profit_change:+,.0f}",
        help="BakeSmart simulated profit minus fixed-plan simulated profit.",
    )

    monthly = (
        simulation.set_index("date")[
            ["estimated_waste", "lost_sales", "estimated_profit"]
        ]
        .resample("ME")
        .sum()
    )
    st.markdown("### Monthly surplus and missed demand")
    st.line_chart(monthly[["estimated_waste", "lost_sales"]])

with portfolio_tab:
    st.markdown(
        '<div class="section-kicker">Portfolio overview</div>',
        unsafe_allow_html=True,
    )
    st.markdown("### Compare the bakery's three leading products")
    st.write(
        "This view helps management see which products drive volume, revenue, "
        "and operational uncertainty."
    )

    portfolio_rows = []
    for portfolio_product in products:
        history = daily_sales[daily_sales["product"] == portfolio_product]
        product_sales = sales[sales["article"] == portfolio_product]
        product_price = typical_price(sales, portfolio_product)
        weekday_means = history.groupby("weekday")["units_sold"].mean()
        average_daily = history["units_sold"].mean()
        variability = (
            history["units_sold"].std() / average_daily * 100
            if average_daily
            else 0
        )
        portfolio_rows.append(
            {
                "Product": portfolio_product.title(),
                "Total units": history["units_sold"].sum(),
                "Average per day": average_daily,
                "Typical price (EUR)": product_price,
                "Recorded revenue (EUR)": (
                    product_sales["Quantity"] * product_sales["unit_price_eur"]
                ).sum(),
                "Strongest weekday": weekday_means.idxmax(),
                "Variability": variability,
            }
        )

    portfolio = pd.DataFrame(portfolio_rows).sort_values(
        "Recorded revenue (EUR)", ascending=False
    )
    revenue_leader = portfolio.iloc[0]
    volume_leader = portfolio.sort_values("Total units", ascending=False).iloc[0]
    stable_leader = portfolio.sort_values("Variability").iloc[0]

    st.markdown(
        '<div class="kpi-grid three">'
        + kpi_card(
            "Revenue leader",
            revenue_leader["Product"],
            f"EUR {revenue_leader['Recorded revenue (EUR)']:,.0f} recorded",
            "coins",
            "caramel",
        )
        + kpi_card(
            "Volume leader",
            volume_leader["Product"],
            f"{volume_leader['Total units']:,.0f} units sold",
            "basket",
            "blue",
        )
        + kpi_card(
            "Most predictable",
            stable_leader["Product"],
            f"{stable_leader['Variability']:.0f}% demand variability",
            "target",
            "sage",
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    display_portfolio = portfolio.copy()
    display_portfolio["Variability"] = display_portfolio["Variability"].map(
        lambda value: f"{value:.0f}%"
    )
    st.dataframe(
        display_portfolio.style.format(
            {
                "Total units": "{:,.0f}",
                "Average per day": "{:,.1f}",
                "Typical price (EUR)": "{:.2f}",
                "Recorded revenue (EUR)": "{:,.0f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    portfolio_chart = portfolio.set_index("Product")[
        ["Total units", "Recorded revenue (EUR)"]
    ]
    st.markdown("### Product scale comparison")
    st.bar_chart(portfolio_chart)

with method_tab:
    st.markdown(
        """
        <div class="section-kicker">Transparent methodology</div>

        ### The logic in three steps

        1. BakeSmart adds up how many units of the selected product were sold each day.
        2. It finds the average for the same weekday. A Tuesday forecast therefore
           uses all historical Tuesdays.
        3. It adds the chosen safety buffer and rounds to a whole production quantity.

        **Profit formula:** expected sales x selling price - recommended production x
        production cost.

        ### Important limitation

        The source contains sales, not inventory or discarded food. Surplus, missed
        demand, production cost, and profit are therefore transparent simulations,
        not measured facts. This prototype supports a business decision; it does not
        claim to know the bakery's real waste.

        ### Benchmark used

        The business simulation compares BakeSmart with a simple fixed plan that
        prepares the same average quantity on every observed trading day. Dates with
        no bakery transactions are treated as closed days rather than zero-demand days.
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.caption(
    f"Source: French Bakery Daily Sales dataset | "
    f"{len(sales):,} valid transaction rows | "
    f"{sales['date'].min():%d %b %Y} to {sales['date'].max():%d %b %Y}"
)
