from date_utils import increase_date_by_day
from constants import DATE_FORMAT, DATABASE_PATH
from printing_utils import print_error_saving_into_database
from api_utils import fetch_share_prices_from_yahoo_finance_api
from constants import GOOGLE_SPREADSHEET_DATA_FILE, SQL_QUERY_CREATE_TABLE_FINANCIALS, SQL_QUERY_CREATE_TABLE_SHARE_PRICES, SQL_QUERY_SAVE_FINANCIALS, SQL_QUERY_SAVE_SHARE_PRICES, SQL_QUERY_READ_ALL_FINANCIALS, SQL_QUERY_READ_ALL_SHARE_PRICES
from config import START_DATE, END_DATE
import csv
import sqlite3 as sl

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
    _read_all_data_from_database()

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
                currency = 'USD' # Hardcoded
                # Todo: numbers are in thousands - fix it
                data_to_save.append([row[0], row[1], currency, int(row[2].replace(',', '')), int(row[3].replace(',', ''))])
    return data_to_save

def _save_financial_data(data):
    for report in data:
        ticker = report[0]
        filling_date = report[1]
        currency = report[2]
        free_cash_flow = report[3]
        amount_of_shares = report[4]
        sql = SQL_QUERY_SAVE_FINANCIALS
        data = (ticker, filling_date, currency, free_cash_flow, amount_of_shares)
        _save_fetched_data_into_database(sql, data)

def _save_share_prices_data(data, date_format = DATE_FORMAT):
    for index, row in data.iterrows():
        date = index.strftime(date_format)
        averaged_price = (row["High"] + row["Low"]) / 2
        # Always USD in case of share prices fetched from Yahoo through Data Reader - MAY BE OUTDATED INFO.
        data = (row["Ticker"], date, "USD", averaged_price)
        _save_fetched_data_into_database(SQL_QUERY_SAVE_SHARE_PRICES, data)

def _save_fetched_data_into_database(sql_query, data):
    con = sl.connect(DATABASE_PATH)
    with con:
        try:
            con.execute(sql_query, data)
        except Exception as e:
            print(f"Error in save_fetched_data_into_database: {e}")

def _read_all_data_from_database():
    con = sl.connect(DATABASE_PATH)
    with con:
        data = con.execute(SQL_QUERY_READ_ALL_FINANCIALS)
        print("DATABASE TEST: FINANCIALS")
        for row in data:
            print(row)
        data = con.execute(SQL_QUERY_READ_ALL_SHARE_PRICES)
        print("DATABASE TEST: SHARE_PRICES")
        for row in data:
            print(row)

def get_most_recent_income_statement_for_given_company_for_given_date_company_outlook_n_periods(number_of_periods, company_ticker, date):
    most_recent_income_statements_for_this_date = []
    con = sl.connect(DATABASE_PATH)
    with con:
        data = con.execute("SELECT * FROM FINANCIALS WHERE ticker = '" + company_ticker + "'" + " AND filling_date <= '" + date + "' ORDER BY filling_date DESC LIMIT '" + str(number_of_periods) + "'")
        most_recent_income_statements_for_this_date = data.fetchall()
    return most_recent_income_statements_for_this_date

def read_share_prices_per_particular_period(company, start_date, end_date):
    con = sl.connect(DATABASE_PATH)
    data = []
    with con:
        data = con.execute("SELECT * FROM SHARE_PRICES WHERE ticker = '" + company + "' AND date >='" + start_date + "' AND date <='" + end_date + "'")
    values_to_export = []
    for row in data.fetchall():
        values_to_export.append((row[1], row[3]))
    return values_to_export

def try_to_fetch_prices_in_particular_period(company, start_date, end_date, is_it_last_sub_period):
    share_prices_table = read_share_prices_per_particular_period(company, start_date, end_date)
    if is_it_last_sub_period is False:
        end_date_variable = end_date
        # I want to try to increase 4 times, on 5th attempt - print error. The loop works in 0 - (n-1) range.
        AMOUNT_OF_DATE_INCREASE_TRIES = 4
        for i in range(0, (AMOUNT_OF_DATE_INCREASE_TRIES + 1)):
            last_date = share_prices_table[-1][0]
            if last_date >=end_date:
                break
            else:
                if i < AMOUNT_OF_DATE_INCREASE_TRIES:
                    end_date_variable = increase_date_by_day(end_date_variable, DATE_FORMAT)
                    share_prices_table = read_share_prices_per_particular_period(company, start_date, end_date_variable)
                else:
                    share_prices_table = None
                    print("ERROR: End date increased 4 times and still couldn't be read.")
    return [[row[1] for row in share_prices_table]]

def read_db_share_price_in_particular_day(company, date):
    fetched_share_price_data = try_to_fetch_prices_in_particular_period(company, date, date, True)
    if len(fetched_share_price_data[0]) == 0:
        return None
    else:
        return fetched_share_price_data[0][0]
