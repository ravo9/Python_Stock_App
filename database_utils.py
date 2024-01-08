import sqlite3 as sl
from date_utils import increase_date_by_day
from constants import DATE_FORMAT
from printing_utils import print_error_saving_into_database
import csv


SQL_QUERY_CREATE_TABLE_INCOME_STATEMENTS = """CREATE TABLE IF NOT EXISTS INCOME_STATEMENT (ticker TEXT, currency TEXT, filling_date DATE, eps FLOAT, epsDiluted FLOAT, PRIMARY KEY (ticker, filling_date));"""
SQL_QUERY_CREATE_TABLE_COMPANY_OUTLOOK = """CREATE TABLE IF NOT EXISTS COMPANY_OUTLOOK (ticker TEXT, filling_date DATE, currency TEXT, freeCashFlow FLOAT, amountOfShares INT, PRIMARY KEY (ticker, filling_date));"""
SQL_QUERY_CREATE_TABLE_SHARE_PRICES = """CREATE TABLE IF NOT EXISTS SHARE_PRICES (ticker TEXT, date DATE, currency TEXT, price FLOAT, PRIMARY KEY (ticker, date));"""

SQL_QUERY_SAVE_INCOME_STATEMENTS = 'INSERT INTO INCOME_STATEMENT (ticker, currency, filling_date, eps, epsDiluted) values(?, ?, ?, ?, ?)'
SQL_QUERY_SAVE_COMPANY_OUTLOOK = 'INSERT INTO COMPANY_OUTLOOK (ticker, filling_date, currency, freeCashFlow, amountOfShares) values(?, ?, ?, ?, ?)'
SQL_QUERY_SAVE_SHARE_PRICES = 'INSERT INTO SHARE_PRICES (ticker, date, currency, price) values(?, ?, ?, ?)'

SQL_QUERY_READ_ALL_INCOME_STATEMENTS = 'SELECT * FROM INCOME_STATEMENT'
SQL_QUERY_READ_ALL_COMPANY_OUTLOOK = 'SELECT * FROM COMPANY_OUTLOOK'
SQL_QUERY_READ_ALL_SHARE_PRICES = 'SELECT * FROM SHARE_PRICES'


def initialize_database():
    con = sl.connect('database.db')
    with con:
        con.execute(SQL_QUERY_CREATE_TABLE_INCOME_STATEMENTS)
        con.execute(SQL_QUERY_CREATE_TABLE_COMPANY_OUTLOOK)
        con.execute(SQL_QUERY_CREATE_TABLE_SHARE_PRICES)


# Todo: Dates and FCF are currently stored as strings.
def import_and_process_csv(file_path):
    data_to_save = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row
        for row in reader:
            if row:  # Check if the row is not empty
                # Assuming the currency is always in USD and amount_of_shares is not provided in the CSV
                currency = 'USD'
                # Todo: some numbers are in thousands - fix it
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


# def save_fetched_data_into_database_income_statements(data, debug_mode = False):
    # for income_statement in data:
        # eps = income_statement['eps']
        # eps_diluted = income_statement['epsdiluted']


def save_fetched_data_into_database_share_prices(data, date_format, debug_mode = False):
    for index, row in data.iterrows():
        date = index.strftime(date_format)
        ticker = row["Ticker"]
        high_price = row["High"]
        low_price = row["Low"]
        averaged_price = (high_price + low_price) / 2
        # Always USD in case of share prices fetched from Yahoo through Data Reader
        currency = "USD"

        sql = SQL_QUERY_SAVE_SHARE_PRICES
        data = (ticker, date, currency, averaged_price)
        save_fetched_data_into_database(sql, data, debug_mode)


def save_fetched_data_into_database(sql_query, data, debug_mode = False):
    con = sl.connect('database.db')
    with con:
        try:
            con.execute(sql_query, data)
        except:
            print_error_saving_into_database(sql_query, data, debug_mode)


def read_all_data_from_database():
    con = sl.connect('database.db')
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
    con = sl.connect('database.db')
    with con:
        data = con.execute("SELECT * FROM COMPANY_OUTLOOK WHERE ticker = '" + company_ticker + "'" + " AND filling_date <= '" + date + "' ORDER BY filling_date DESC LIMIT '" + str(number_of_periods) + "'")
        most_recent_income_statements_for_this_date = data.fetchall()
    return most_recent_income_statements_for_this_date


def get_most_recent_income_statement_for_given_company_for_given_date_n_periods(number_of_periods, company_ticker, date, debug_mode = False):
    most_recent_income_statements_for_this_date = []
    con = sl.connect('database.db')
    with con:
        data = con.execute("SELECT * FROM INCOME_STATEMENT WHERE ticker = '" + company_ticker + "'" + " AND filling_date <= '" + date + "' ORDER BY filling_date DESC LIMIT '" + str(number_of_periods) + "'")
        most_recent_income_statements_for_this_date = data.fetchall()
    return most_recent_income_statements_for_this_date


def get_most_recent_income_statement_for_given_company_for_given_date(company_ticker, date, debug_mode = False):
    most_recent_income_statement_for_this_date = None
    con = sl.connect('database.db')
    with con:
        data = con.execute("SELECT * FROM INCOME_STATEMENT WHERE ticker = '" + company_ticker + "'" + " AND filling_date <= '" + date + "' ORDER BY filling_date DESC LIMIT 1")
        most_recent_income_statement_for_this_date = data.fetchone()
    return most_recent_income_statement_for_this_date


def read_share_prices_per_particular_period(company, start_date, end_date):
    con = sl.connect('database.db')
    data = []
    with con:
        data = con.execute("SELECT * FROM SHARE_PRICES WHERE ticker = '" + company + "' AND date >='" + start_date + "' AND date <='" + end_date + "'")
    values_to_export = []
    for row in data.fetchall():
        values_to_export.append((row[1], row[3]))
    return values_to_export


def try_to_fetch_prices_in_particular_period(company, start_date, end_date, is_it_last_sub_period, debug_mode):
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
                    end_date_variable = increase_date_by_day(end_date_variable, DATE_FORMAT, debug_mode)
                    share_prices_table = read_share_prices_per_particular_period(company, start_date, end_date_variable)
                else:
                    share_prices_table = None
                    print("ERROR: End date increased 4 times and still couldn't be read.")

    values_to_export = [[]]
    for row in share_prices_table:
        values_to_export[0].append(row[1])
    return values_to_export


def read_db_share_price_in_particular_day(company, date, debug_mode):
    fetched_share_price_data = try_to_fetch_prices_in_particular_period(company, date, date, True, debug_mode)
    if len(fetched_share_price_data[0]) == 0:
        return None
    else:
        return fetched_share_price_data[0][0]
