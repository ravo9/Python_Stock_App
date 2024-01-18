import pandas
import yfinance as yf
import requests
from config import AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH
from datetime import datetime, timedelta

API_ENDPOINT = "https://api.polygon.io/vX/reference/financials"
API_KEY = "KJSvMYzpmGOzks95qGHHL4THnEztfEbm"

def fetch_financial_data_for_given_companies(companies):
    # return [
    #     (response.json(), company)
    #     for company in companies
    #     if (response := requests.get(API_ENDPOINT, params={
    #         "apiKey": API_KEY,
    #         "ticker": company,
    #         "limit": AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH + 1
    #         # quarter vs annually
    #     })).ok
    # ]
    results = []
    for company in companies:
        try:
            response = requests.get(API_ENDPOINT, params={
                "apiKey": API_KEY,
                "ticker": company,
                "limit": AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH + 1
            })
            if response.ok:
                results.append((response.json(), company))
            else:
                print(f"Error fetching data for {company}: {response.status_code} - {response.reason}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {company}: {e}")
    return results

def fetch_price_in_particular_day_dynamically(company, date):
    for _ in range(5):
        share_prices_table = yf.download(company, start=date, end=(datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)), progress=False)
        if not share_prices_table.empty:
            averaged_price = (share_prices_table["High"] + share_prices_table["Low"]) / 2
            final_results = averaged_price.tolist()
            return final_results[0]
        date = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
    raise ValueError("No data available for the specified date after 5 attempts.")

def fetch_price_in_particular_period_dynamically(company, start_date, end_date):
    end_date = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
    if not share_prices_table.empty:
        averaged_prices = (share_prices_table["High"] + share_prices_table["Low"]) / 2
        result = [averaged_prices.tolist()]
        return result
    raise ValueError("No data available for the specified date after 5 attempts.")

# todo: optimise
# todo: sometimes missing very last few days data.
def fetch_total_amount_of_shares_on_particular_day(company, date):
    try:
        shares_data = yf.Ticker(company).get_shares_full(start=date)
        if shares_data is None:
            raise ValueError(f"No data returned for company {company} on {date}")
        return shares_data[0]
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching shares data: {e}")
