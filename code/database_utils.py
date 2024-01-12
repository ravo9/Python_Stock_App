from date_utils import increase_date_by_day
from constants import DATE_FORMAT, DATABASE_PATH
from api_utils import fetch_share_prices_from_yahoo_finance_api
from constants import GOOGLE_SPREADSHEET_DATA_FILE, SQL_QUERY_CREATE_TABLE_FINANCIALS, SQL_QUERY_CREATE_TABLE_SHARE_PRICES, SQL_QUERY_SAVE_FINANCIALS, SQL_QUERY_SAVE_SHARE_PRICES, SQL_QUERY_READ_ALL_FINANCIALS, SQL_QUERY_READ_ALL_SHARE_PRICES, SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS
from config import START_DATE, END_DATE
import csv
import sqlite3 as sl
from datetime import datetime

def find_share_price_for_this_date(date, company_ticker):
    share_price_for_this_date = None
    date_variable = date
    attempt = 0
    while share_price_for_this_date is None and attempt < 5:
        share_price_for_this_date = _read_db_share_price_in_particular_day(company_ticker, date_variable)
        if share_price_for_this_date is None:
            date_variable = increase_date_by_day(date_variable, DATE_FORMAT)
        attempt += 1
    if share_price_for_this_date is None:
        raise ValueError("ERROR: Could not find share price after 5 attempts.")
    return share_price_for_this_date

def fetch_necessary_data_for_experiment(companies):
    _initialize_database()
    _save_financial_data(_fetch_financial_data_from_google_sheets_csv(
        GOOGLE_SPREADSHEET_DATA_FILE
    ))
    _save_share_prices_data(fetch_share_prices_from_yahoo_finance_api(
        companies,
        START_DATE,
        END_DATE
    ))
    # _read_all_data_from_database()

def fetch_related_financial_reports(number_of_periods, company_ticker, date):
    con = sl.connect(DATABASE_PATH)
    with con:
        most_recent_financial_reports_for_this_date = (con.execute(SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS, (company_ticker, date, number_of_periods))).fetchall()
    if most_recent_financial_reports_for_this_date == []:
        raise ValueError("ERROR: Empty list")
    return most_recent_financial_reports_for_this_date

def try_to_fetch_prices_in_particular_period(company, start_date, end_date, is_it_last_sub_period):
    share_prices_table = _read_share_prices_per_particular_period(company, start_date, end_date)
    if not is_it_last_sub_period:
        AMOUNT_OF_DATE_INCREASE_TRIES = 4
        end_date_variable = end_date
        for i in range(AMOUNT_OF_DATE_INCREASE_TRIES + 1):
            last_date = share_prices_table[-1][0]
            if last_date >= end_date:
                break
            if i == AMOUNT_OF_DATE_INCREASE_TRIES:
                print("ERROR: End date increased 4 times and still couldn't be read.")
                return None
            end_date_variable = increase_date_by_day(end_date_variable, DATE_FORMAT)
            share_prices_table = _read_share_prices_per_particular_period(company, start_date, end_date_variable)
    return [[row[1] for row in share_prices_table]]

def _initialize_database():
    con = sl.connect(DATABASE_PATH)
    with con:
        con.execute(SQL_QUERY_CREATE_TABLE_FINANCIALS)
        con.execute(SQL_QUERY_CREATE_TABLE_SHARE_PRICES)

def _fetch_financial_data_from_google_sheets_csv(file_path):
    data_to_save = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row
        for row in reader:
            if row:
                data_to_save.append([row[0], row[1], 'USD', int(row[2].replace(',', '')), int(row[3].replace(',', ''))]) # Todo: "numbers are in thousands"; hard-coded currency;
    return data_to_save

def _save_financial_data(data):
    for report in data:
        ticker = report[0]
        filling_date_formatted = (datetime.strptime(report[1], "%m/%d/%Y")).strftime("%Y-%m-%d")
        currency = report[2]
        free_cash_flow = report[3]
        amount_of_shares = report[4]
        data = (ticker, filling_date_formatted, currency, free_cash_flow, amount_of_shares)
        _save_fetched_data_into_database(SQL_QUERY_SAVE_FINANCIALS, data)

def _save_share_prices_data(data, date_format = DATE_FORMAT):
    for index, row in data.iterrows():
        date = index.strftime(date_format)
        averaged_price = (row["High"] + row["Low"]) / 2
        data = (row["Ticker"], date, "USD", averaged_price) # Alawys USD - not sure if correct;
        _save_fetched_data_into_database(SQL_QUERY_SAVE_SHARE_PRICES, data)

def _save_fetched_data_into_database(sql_query, data):
    try:
        (sl.connect(DATABASE_PATH)).execute(sql_query, data)
    except Exception as e:
        print("Error in save_fetched_data_into_database: {e}")

def _read_all_data_from_database():
    queries = {
        "DATABASE TEST: FINANCIALS": SQL_QUERY_READ_ALL_FINANCIALS,
        "DATABASE TEST: SHARE_PRICES": SQL_QUERY_READ_ALL_SHARE_PRICES
    }
    with sl.connect(DATABASE_PATH) as con:
        for label, query in queries.items():
            print(label)
            for row in con.execute(query):
                print(row)

def _read_share_prices_per_particular_period(company, start_date, end_date):
    con = sl.connect(DATABASE_PATH)
    data = []
    with con:
        data = con.execute("SELECT * FROM SHARE_PRICES WHERE ticker = '" + company + "' AND date >='" + start_date + "' AND date <='" + end_date + "'")
    return [(row[1], row[3]) for row in data.fetchall()]

def _read_db_share_price_in_particular_day(company, date):
    fetched_share_price_data = try_to_fetch_prices_in_particular_period(company, date, date, True)
    return None if len(fetched_share_price_data[0]) == 0 else fetched_share_price_data[0][0]
