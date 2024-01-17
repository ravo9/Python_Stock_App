import pandas
import yfinance as yf
import requests
from config import AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH

API_ENDPOINT = "https://api.polygon.io/vX/reference/financials"
API_KEY = "KJSvMYzpmGOzks95qGHHL4THnEztfEbm"

def fetch_financial_data_for_given_companies(companies):
    return [
        (response.json(), company)
        for company in companies
        if (response := requests.get(API_ENDPOINT, params={
            "apiKey": API_KEY,
            "ticker": company,
            "limit": AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH + 1
            # quarter vs annually
        })).ok
    ]

# todo: optimise
def fetch_total_amount_of_shares_on_particular_day(company, date):
    try:
        shares_data = yf.Ticker(company).get_shares_full(start=date)
        print(shares_data)
        if shares_data is None:
            raise ValueError(f"No data returned for company {company} on {date}")
        return shares_data[0]
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching shares data: {e}")

def fetch_share_prices_from_yfinance(companies, start_date, end_date):
    fetched_prices = []
    table_columns_to_be_fetched = ["High", "Low"]
    for company in companies:
        share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
        values = share_prices_table.filter(table_columns_to_be_fetched)
        fetched_prices.append(values.assign(Ticker=company))
    return pandas.concat(fetched_prices)
