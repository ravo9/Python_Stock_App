import yfinance as yf
from datetime import datetime, timedelta
from database_utils import save_shares_amount_data, save_share_price_daily_data, save_share_prices_in_period_data
import contextlib
import os

def fetch_share_price_daily(company, date, date_format = "%Y-%m-%d"):
    for _ in range(5):
        with open(os.devnull, 'w') as devnull, contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull): # Mutes yfinance exceptions that are already handled.
            share_prices_table = yf.download(company, start=date, end=(datetime.strptime(date, date_format) + timedelta(days=1)), progress=False)
            if not share_prices_table.empty:
                share_price = ((share_prices_table["High"] + share_prices_table["Low"]) / 2).tolist()[0]
                save_share_price_daily_data(share_price, company, date) # Caching
                return share_price
            date = (datetime.strptime(date, date_format) - timedelta(days=1)).strftime(date_format)
    raise ValueError("No data available for the specified date after 5 attempts.")

def fetch_share_prices_per_period(company, start_date, end_date, date_format = "%Y-%m-%d"):
    share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
    if not share_prices_table.empty:
        averaged_prices = [((share_prices_table["High"] + share_prices_table["Low"]) / 2).tolist()]
        save_share_prices_in_period_data(company, start_date, end_date, json.dumps(averaged_prices)) # Caching
        return averaged_prices
    raise ValueError("No data available for the specified date after 5 attempts.")

def fetch_total_amount_of_shares_on_particular_day(company, date):
    attempts = 0;
    while attempts < 3:
        try:
            value = yf.Ticker(company).get_shares_full(start=date)[0] # Throws exception if no data found
            save_shares_amount_data(value, company, date) # Caching
            return value
        except Exception as e:
            # print(f"No data returned for company {company} on {date} attempt {attempts + 1}")
            date -= timedelta(weeks=1)
            attempts += 1
    return None
