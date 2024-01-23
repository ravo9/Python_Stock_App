import yfinance as yf
from datetime import datetime, timedelta
from database_utils import save_financial_data, save_data_to_database, get_stored_reports_raw, SQL_QUERY_CREATE_TABLE_SHARE_PRICE, SQL_QUERY_INSERT_SHARE_PRICE, SQL_QUERY_CREATE_TABLE_SHARES_AMOUNT, SQL_QUERY_INSERT_SHARES_AMOUNT, SQL_QUERY_CREATE_TABLE_SHARE_PRICES_IN_PERIOD, SQL_QUERY_INSERT_SHARE_PRICE_PERIOD
import contextlib
import requests
import os
import json
import time

# API_ENDPOINT = "https://api.polygon.io/vX/reference/financials"
# API_KEY = "KJSvMYzpmGOzks95qGHHL4THnEztfEbm"
API_ENDPOINT = "https://financialmodelingprep.com/api/v3/cash-flow-statement/"
API_KEY = "ee22bac37cfc64407760039b37d56065"
DOWNLOADING_FROM_POLYGON_ACC = 0

def fetch_financial_reports(ticker, number_of_reports_for_calculations, number_of_reports_to_fetch, date):
    try:
        _hold_download_if_necessary()
        print("DOWNLOADING: " + ticker)
        response = requests.get((API_ENDPOINT + ticker), params={"apikey": API_KEY, "period": "quarterly"})
        save_financial_data(response.json(), ticker) if response.ok else print(f"Error fetching data: {ticker}: {response.status_code} - {response.reason}")
        recent_reports = get_stored_reports_raw(ticker, date, number_of_reports_for_calculations)
        if not recent_reports: raise ValueError("ERROR: Empty list")
        return recent_reports
    except Exception as e: print(f"Error fetch_financial_reports: Request failed: {ticker} - {e}")

def _hold_download_if_necessary():
    global DOWNLOADING_FROM_POLYGON_ACC
    if (DOWNLOADING_FROM_POLYGON_ACC == 5):
        # print("WAITING FOR DOWNLOAD 60 SECONDS")
        # time.sleep(60)
        DOWNLOADING_FROM_POLYGON_ACC = 0
    DOWNLOADING_FROM_POLYGON_ACC += 1

def fetch_share_price_daily(company, date, date_format = "%Y-%m-%d"):
    for _ in range(5):
        with open(os.devnull, 'w') as devnull, contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull): # Mutes yfinance exceptions that are already handled.
            share_prices_table = yf.download(company, start=date, end=(datetime.strptime(date, date_format) + timedelta(days=1)), progress=False)
            if not share_prices_table.empty:
                share_price = _turn_price_table_into_average_price(share_prices_table)[0]
                save_data_to_database(SQL_QUERY_CREATE_TABLE_SHARE_PRICE, SQL_QUERY_INSERT_SHARE_PRICE, float(share_price), company, date) # Caching
                return share_price
            date = (datetime.strptime(date, date_format) - timedelta(days=1)).strftime(date_format)
    raise ValueError("No data available for the specified date after 5 attempts.")

def fetch_share_prices_per_period(company, start_date, end_date, date_format = "%Y-%m-%d"):
    share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
    if not share_prices_table.empty:
        averaged_prices = [_turn_price_table_into_average_price(share_prices_table)]
        save_data_to_database(SQL_QUERY_CREATE_TABLE_SHARE_PRICES_IN_PERIOD, SQL_QUERY_INSERT_SHARE_PRICE_PERIOD, company, start_date, end_date, json.dumps(averaged_prices)) # Caching
        return averaged_prices
    raise ValueError("Error fetch_share_prices_per_period: share_prices_table empty")

def _turn_price_table_into_average_price(share_prices_table): return ((share_prices_table["High"] + share_prices_table["Low"]) / 2).tolist()

def fetch_total_amount_of_shares_on_particular_day(company, date):
    for attempt in range(3):
        try:
            value = yf.Ticker(company).get_shares_full(start=date)[0] # Throws exception if no data found
            save_data_to_database(SQL_QUERY_CREATE_TABLE_SHARES_AMOUNT, SQL_QUERY_INSERT_SHARES_AMOUNT, int(value), company, date) # Caching
            return value
        except Exception as e:
            print(f"No data returned for company {company} on {date} attempt {attempt + 1} {e}")
            date -= timedelta(weeks=1)
    return None
