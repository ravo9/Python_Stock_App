import yfinance as yf
import requests
from config import NUMBER_OF_REPORTS_TO_FETCH_FROM_API
from datetime import datetime, timedelta
from database_utils import check_if_these_reports_are_already_stored
import contextlib
import os

API_ENDPOINT = "https://api.polygon.io/vX/reference/financials"
API_KEY = "KJSvMYzpmGOzks95qGHHL4THnEztfEbm"

# NUMBER_OF_REPORTS_TO_FETCH_FROM_API doesn't work precisely. Sometimes fetches 1 or few reports less than should.
def fetch_financial_data(companies):
    NUMBER_OF_REPORTS_TO_FETCH_FROM_API_ADJUSTED = NUMBER_OF_REPORTS_TO_FETCH_FROM_API + 1
    for company in companies:
        try:
            if (check_if_these_reports_are_already_stored(company, NUMBER_OF_REPORTS_TO_FETCH_FROM_API_ADJUSTED)):
                print(f"Reports already exist for {company}")
                continue
            response = requests.get(API_ENDPOINT, params={"apiKey": API_KEY, "ticker": company, "limit": NUMBER_OF_REPORTS_TO_FETCH_FROM_API_ADJUSTED})
            yield (response.json(), company) if response.ok else print(f"Error fetching data: {company}: {response.status_code} - {response.reason}")
        except Exception as e: print(f"Request failed: {company} - {e}")

def fetch_price_in_particular_day_dynamically(company, date, date_format = "%Y-%m-%d"):
    for _ in range(5):
        with open(os.devnull, 'w') as devnull, contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull): # Mutes yfinance exceptions that are already handled.
            share_prices_table = yf.download(company, start=date, end=(datetime.strptime(date, date_format) + timedelta(days=1)), progress=False)
            if not share_prices_table.empty: return ((share_prices_table["High"] + share_prices_table["Low"]) / 2).tolist()[0]
            date = (datetime.strptime(date, date_format) - timedelta(days=1)).strftime(date_format)
    raise ValueError("No data available for the specified date after 5 attempts.")

def fetch_price_in_particular_period_dynamically(company, start_date, end_date, date_format = "%Y-%m-%d"):
    end_date = (datetime.strptime(end_date, date_format) + timedelta(days=1)).strftime(date_format)
    share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
    if not share_prices_table.empty:
        averaged_prices = (share_prices_table["High"] + share_prices_table["Low"]) / 2
        return [averaged_prices.tolist()]
    raise ValueError("No data available for the specified date after 5 attempts.")

# Todo: optimise (not reason to fetch this whole table).
# Todo: this is making problems with current date as date - delay around 10 days sometimes
def fetch_total_amount_of_shares_on_particular_day(company, date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    attempts = 0
    while attempts < 3:
        try:
            return yf.Ticker(company).get_shares_full(start=date.strftime('%Y-%m-%d'))[0] # Throws exception if no data found
        except Exception as e:
            print(f"No data returned for company {company} on {date} attempt {attempts + 1}")
            date -= timedelta(weeks=1)
            attempts += 1
    return None
