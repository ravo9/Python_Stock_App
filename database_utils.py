from date_utils import increase_date_by_day
from constants import DATE_FORMAT
from printing_utils import print_error_saving_into_database
from constants import SQL_QUERY_CREATE_TABLE_INCOME_STATEMENTS, SQL_QUERY_CREATE_TABLE_COMPANY_OUTLOOK, SQL_QUERY_CREATE_TABLE_SHARE_PRICES, SQL_QUERY_SAVE_INCOME_STATEMENTS, SQL_QUERY_SAVE_COMPANY_OUTLOOK, SQL_QUERY_SAVE_SHARE_PRICES, SQL_QUERY_READ_ALL_INCOME_STATEMENTS, SQL_QUERY_READ_ALL_COMPANY_OUTLOOK, SQL_QUERY_READ_ALL_SHARE_PRICES
import csv
import sqlite3 as sl

DATABASE_PATH = "database.db"

def initialize_database():
    con = sl.connect(DATABASE_PATH)
    with con:
        con.execute(SQL_QUERY_CREATE_TABLE_INCOME_STATEMENTS)
        con.execute(SQL_QUERY_CREATE_TABLE_COMPANY_OUTLOOK)
        con.execute(SQL_QUERY_CREATE_TABLE_SHARE_PRICES)

def import_and_process_csv(file_path):
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

def save_fetched_data_into_database_google_sheets_data(data, debug_mode = False):
    for report in data:
        ticker = report[0]
        filling_date = report[1]
        currency = report[2]
        free_cash_flow = report[3]
        amount_of_shares = report[4]
        sql = SQL_QUERY_SAVE_COMPANY_OUTLOOK
        data = (ticker, filling_date, currency, free_cash_flow, amount_of_shares)
        save_fetched_data_into_database(sql, data, debug_mode)

def save_fetched_data_into_database_share_prices(data, date_format, debug_mode = False):
    for index, row in data.iterrows():
        date = index.strftime(date_format)
        averaged_price = (row["High"] + row["Low"]) / 2
        # Always USD in case of share prices fetched from Yahoo through Data Reader - MAY BE OUTDATED INFO.
        data = (row["Ticker"], date, "USD", averaged_price)
        save_fetched_data_into_database(SQL_QUERY_SAVE_SHARE_PRICES, data, debug_mode)

def save_fetched_data_into_database(sql_query, data, debug_mode = False):
    con = sl.connect(DATABASE_PATH)
    with con:
        try:
            con.execute(sql_query, data)
        except:
            print_error_saving_into_database(sql_query, data, debug_mode)

def read_all_data_from_database():
    con = sl.connect(DATABASE_PATH)
    with con:
        data = con.execute(SQL_QUERY_READ_ALL_INCOME_STATEMENTS)
        print("DATABASE TEST: INCOME_STATEMENT")
        for row in data:
            print(row)
        data = con.execute(SQL_QUERY_READ_ALL_COMPANY_OUTLOOK)
        print("DATABASE TEST: COMPANY_OUTLOOK")
        for row in data:
            print(row)
        data = con.execute(SQL_QUERY_READ_ALL_SHARE_PRICES)
        print("DATABASE TEST: SHARE_PRICES")
        for row in data:
            print(row)

def get_most_recent_income_statement_for_given_company_for_given_date_company_outlook_n_periods(number_of_periods, company_ticker, date, debug_mode = False):
    most_recent_income_statements_for_this_date = []
    con = sl.connect(DATABASE_PATH)
    with con:
        data = con.execute("SELECT * FROM COMPANY_OUTLOOK WHERE ticker = '" + company_ticker + "'" + " AND filling_date <= '" + date + "' ORDER BY filling_date DESC LIMIT '" + str(number_of_periods) + "'")
        most_recent_income_statements_for_this_date = data.fetchall()
    return most_recent_income_statements_for_this_date

def get_most_recent_income_statement_for_given_company_for_given_date_n_periods(number_of_periods, company_ticker, date, debug_mode = False):
    most_recent_income_statements_for_this_date = []
    con = sl.connect(DATABASE_PATH)
    with con:
        data = con.execute("SELECT * FROM INCOME_STATEMENT WHERE ticker = '" + company_ticker + "'" + " AND filling_date <= '" + date + "' ORDER BY filling_date DESC LIMIT '" + str(number_of_periods) + "'")
        most_recent_income_statements_for_this_date = data.fetchall()
    return most_recent_income_statements_for_this_date

def get_most_recent_income_statement_for_given_company_for_given_date(company_ticker, date, debug_mode = False):
    most_recent_income_statement_for_this_date = None
    con = sl.connect(DATABASE_PATH)
    with con:
        data = con.execute("SELECT * FROM INCOME_STATEMENT WHERE ticker = '" + company_ticker + "'" + " AND filling_date <= '" + date + "' ORDER BY filling_date DESC LIMIT 1")
        most_recent_income_statement_for_this_date = data.fetchone()
    return most_recent_income_statement_for_this_date

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
    values_to_export = [[]]
    for row in share_prices_table:
        values_to_export[0].append(row[1])
    return values_to_export

def read_db_share_price_in_particular_day(company, date):
    fetched_share_price_data = try_to_fetch_prices_in_particular_period(company, date, date, True)
    if len(fetched_share_price_data[0]) == 0:
        return None
    else:
        return fetched_share_price_data[0][0]
