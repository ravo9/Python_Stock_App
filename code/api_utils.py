import pandas
import yfinance as yf
import requests

# As it's paid, I don't wanna the app to be dependent on it. I wanna use the API
# temporarily, scrap data, and then use this DB offline.
API_ENDPOINT = "https://api.polygon.io/vX/reference/financials"
API_KEY = "KJSvMYzpmGOzks95qGHHL4THnEztfEbm"
def fetch_database_from_paid_api(company):
    params = {
    "apiKey": API_KEY,
    "ticker": company,
    "limit": (1+4)
    # quarter vs annually
    }
    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_share_prices_from_yahoo_finance_api(companies, start_date, end_date):
    fetched_prices = []
    table_columns_to_be_fetched = ["High", "Low"]
    for company in companies:
        share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
        values = share_prices_table.filter(table_columns_to_be_fetched)
        fetched_prices.append(values.assign(Ticker=company))
    return pandas.concat(fetched_prices)
