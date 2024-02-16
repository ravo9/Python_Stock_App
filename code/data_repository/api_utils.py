import yfinance as yf
from datetime import datetime, timedelta
from .database_utils import save_financial_statements_data, save_data_to_database, get_stored_financial_statements_raw, SQL_CREATE_SHARE_PRICE, SQL_INSERT_SHARE_PRICE, SQL_CREATE_SHARES_AMOUNT, SQL_INSERT_SHARES_AMOUNT, SQL_CREATE_SHARE_PRICES_IN_PERIOD, SQL_INSERT_SHARE_PRICE_PERIOD
import contextlib
import requests
import os
import json

API_ENDPOINT_CASH_FLOW_STATEMENTS = "https://financialmodelingprep.com/api/v3/cash-flow-statement/"
API_ENDPOINT_INCOME_STATEMENTS = "https://financialmodelingprep.com/api/v3/income-statement/"
API_ENDPOINT_BALANCE_SHEETS = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/"
API_KEY = "ee22bac37cfc64407760039b37d56065"

def fetch_financial_statements(statement_type, ticker, number_of_reports_for_calculations, number_of_reports_to_fetch, date):
    api_endpoints = {
        'cash_flow_statement': API_ENDPOINT_CASH_FLOW_STATEMENTS,
        'income_statement': API_ENDPOINT_INCOME_STATEMENTS,
        'balance_sheet': API_ENDPOINT_BALANCE_SHEETS
    }
    try:
        print(f"DOWNLOADING {statement_type.replace('_', ' ').upper()} FOR: {ticker}")
        response = requests.get((api_endpoints[statement_type] + ticker), params={"apikey": API_KEY, "period": "quarterly"})
        if response.ok: save_financial_statements_data(statement_type, response.json(), ticker)
        else: print(f"Error fetching data: {ticker}: {response.status_code} - {response.reason}")
        recent_reports = get_stored_financial_statements_raw(statement_type, ticker, date, number_of_reports_for_calculations)
        if not recent_reports: raise ValueError("ERROR: Empty list")
        return recent_reports
    except Exception as e: print(f"Error fetch_financial_statements {statement_type} : Request failed: {ticker} - {e}")

def fetch_share_price_daily(company, date, date_format = "%Y-%m-%d"):
    for _ in range(5):
        with open(os.devnull, 'w') as devnull, contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull): # Mutes yfinance exceptions that are already handled.
            share_prices_table = yf.download(company, start=date, end=(datetime.strptime(date, date_format) + timedelta(days=1)), progress=False)
            if not share_prices_table.empty:
                share_price = _turn_price_table_into_average_price(share_prices_table)[0]
                save_data_to_database(SQL_CREATE_SHARE_PRICE, SQL_INSERT_SHARE_PRICE, float(share_price), company, date) # Caching
                return share_price
            date = (datetime.strptime(date, date_format) - timedelta(days=1)).strftime(date_format)
    raise ValueError("No data available for the specified date after 5 attempts.")

def fetch_share_prices_per_period(company, start_date, end_date, date_format = "%Y-%m-%d"):
    share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
    if not share_prices_table.empty:
        averaged_prices = [_turn_price_table_into_average_price(share_prices_table)]
        save_data_to_database(SQL_CREATE_SHARE_PRICES_IN_PERIOD, SQL_INSERT_SHARE_PRICE_PERIOD, company, start_date, end_date, json.dumps(averaged_prices)) # Caching
        return averaged_prices
    raise ValueError("Error fetch_share_prices_per_period: share_prices_table empty")

def _turn_price_table_into_average_price(share_prices_table): return ((share_prices_table["High"] + share_prices_table["Low"]) / 2).tolist()

def fetch_total_amount_of_shares_on_particular_day(company, date):
    for attempt in range(3):
        try:
            data = yf.Ticker(company)
            value = data.get_shares_full(start=date)[0] # Throws exception if no data found
            # findSplits(company, data)
            save_data_to_database(SQL_CREATE_SHARES_AMOUNT, SQL_INSERT_SHARES_AMOUNT, int(value), company, date) # Caching
            return value
        except Exception as e:
            print(f"No data returned for company {company} on {date} attempt {attempt + 1} {e}")
            date -= timedelta(weeks=1)
    return None

def findSplits(company, data):
    print("SPLITS FOUND:")
    print(company)
    print(data.get_splits())
