# BakeSmart

BakeSmart is a beginner-friendly Streamlit prototype that recommends how many
bakery products to prepare using historical weekday averages.

## Run the website

Open PowerShell in this folder and run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The browser should open automatically. If it does not, open the local address
shown in PowerShell, usually `http://localhost:8501`.

The required packages are already installed in `.venv` in this project. If that
folder is unavailable on another computer, create a Python environment and
install `requirements.txt` first.

## Data

The app expects:

```text
archive/Bakery sales.csv
```

It automatically selects the three products with the highest total unit sales.

## Forecast

For a selected date, BakeSmart:

1. Finds all historical days with the same weekday.
2. Calculates the selected product's average daily sales.
3. Adds an adjustable safety buffer.
4. Recommends a whole-number production quantity.

The dataset contains sales and prices, but not production costs, inventory, or
waste. Those business outcomes are clearly presented as simulations.

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
