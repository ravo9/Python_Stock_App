from database_utils import get_stored_share_price_value_if_available, get_stored_share_prices_in_period_if_available, get_stored_shares_amount_value_if_available, get_stored_financial_reports_if_available
from api_utils import fetch_share_price_daily, fetch_share_prices_per_period, fetch_total_amount_of_shares_on_particular_day, fetch_financial_reports
from datetime import datetime, timedelta
import json

DATE_FORMAT = "%Y-%m-%d"

def retrieve_financial_reports(number_of_reports_for_calculations, number_of_reports_to_fetch, company_ticker, date):
    stored_value = get_stored_financial_reports_if_available(number_of_reports_for_calculations, number_of_reports_to_fetch, company_ticker, date)
    if stored_value != None: return stored_value
    return fetch_financial_reports(company_ticker, number_of_reports_for_calculations, number_of_reports_to_fetch, date)

def retrieve_share_price_daily(company, date, date_format = DATE_FORMAT):
    stored_value = get_stored_share_price_value_if_available(company, date) # Caching
    if stored_value != None: return stored_value
    return fetch_share_price_daily(company, date, date_format)

def retrieve_share_prices_per_period(company, start_date, end_date, date_format = DATE_FORMAT):
    end_date = (datetime.strptime(end_date, date_format) + timedelta(days=1)).strftime(date_format) # Caching
    stored_value = get_stored_share_prices_in_period_if_available(company, start_date, end_date)
    if stored_value != None: return json.loads(stored_value)
    return fetch_share_prices_per_period(company, start_date, end_date, date_format)

def retrieve_total_amount_of_shares_on_particular_day(company, date_str):
    # Todo: 1. this is making problems with current date as date - delay around 10 days sometimes 2.optimise (not reason to fetch this whole table).
    date = datetime.strptime(date_str, DATE_FORMAT)
    attempts = 0
    stored_value = get_stored_shares_amount_value_if_available(company, date) # Caching
    if stored_value != None: return stored_value  # sometimes was spotted missing in a big dataset (when should've been already cached)
    return fetch_total_amount_of_shares_on_particular_day(company, date)
