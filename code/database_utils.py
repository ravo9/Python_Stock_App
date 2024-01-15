from date_utils import increase_date_by_day
from constants import DATE_FORMAT, DATABASE_PATH
from api_utils import fetch_database_from_paid_api, fetch_share_prices_from_yahoo_finance_api
from constants import GOOGLE_SPREADSHEET_DATA_FILE
from config import START_DATE, END_DATE
import csv
import sqlite3 as sl
from datetime import datetime

PAID_API_DATABASE = 'financial_reports.db'

SQL_QUERY_CREATE_TABLE_BALANCE_SHEET = '''
CREATE TABLE IF NOT EXISTS balance_sheet (
    cik TEXT,
    company_name TEXT,
    end_date TEXT,
    filing_date TEXT,

    assets REAL,
    current_assets REAL,
    current_liabilities REAL,
    equity REAL,
    equity_attributable_to_noncontrolling_interest REAL,
    equity_attributable_to_parent REAL,
    liabilities REAL,

    PRIMARY KEY (company_name, end_date)
)'''
# liabilities_and_equity REAL,
# noncurrent_assets REAL,
# noncurrent_liabilities REAL,
SQL_QUERY_CREATE_TABLE_INCOME_STATEMENT = '''CREATE TABLE IF NOT EXISTS income_statement (cik TEXT, company_name TEXT, end_date TEXT, filing_date TEXT, PRIMARY KEY (company_name, end_date))'''
SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT = '''CREATE TABLE IF NOT EXISTS cash_flow_statement (cik TEXT, company_name TEXT, end_date TEXT, filing_date TEXT, PRIMARY KEY (company_name, end_date))'''
SQL_QUERY_READ_ALL_BALANCE_SHEET = 'SELECT * FROM balance_sheet'
SQL_QUERY_READ_ALL_INCOME_STATEMENT = 'SELECT * FROM income_statement'
SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT = 'SELECT * FROM cash_flow_statement'

SQL_QUERY_CREATE_TABLE_FINANCIALS = """CREATE TABLE IF NOT EXISTS FINANCIALS (ticker TEXT, filling_date DATE, currency TEXT, freeCashFlow FLOAT, amountOfShares INT, PRIMARY KEY (ticker, filling_date));"""
SQL_QUERY_CREATE_TABLE_SHARE_PRICES = """CREATE TABLE IF NOT EXISTS SHARE_PRICES (ticker TEXT, date DATE, currency TEXT, price FLOAT, PRIMARY KEY (ticker, date));"""
SQL_QUERY_SAVE_FINANCIALS = 'INSERT OR REPLACE INTO FINANCIALS (ticker, filling_date, currency, freeCashFlow, amountOfShares) values(?, ?, ?, ?, ?)'
SQL_QUERY_SAVE_SHARE_PRICES = 'INSERT OR REPLACE INTO SHARE_PRICES (ticker, date, currency, price) values(?, ?, ?, ?)'
SQL_QUERY_READ_ALL_FINANCIALS = 'SELECT * FROM FINANCIALS'
SQL_QUERY_READ_ALL_SHARE_PRICES = 'SELECT * FROM SHARE_PRICES'
SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS = 'SELECT * FROM FINANCIALS WHERE ticker = ? AND filling_date <= ? ORDER BY filling_date DESC LIMIT ?'

def steal_data_from_paid_api(companies):
    for company in companies:
        data = fetch_database_from_paid_api(company)
        if data:
            save_database_from_paid_api(data)
    read_database_from_paid_api()

def save_database_from_paid_api(financial_data):
    conn = sl.connect(PAID_API_DATABASE)
    cursor = conn.cursor()

    cursor.execute(SQL_QUERY_CREATE_TABLE_BALANCE_SHEET)
    cursor.execute(SQL_QUERY_CREATE_TABLE_INCOME_STATEMENT)
    cursor.execute(SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT)

    for report in financial_data['results']:
        cik = report['cik'] # Todo: add all properties
        company_name = report['company_name']
        end_date = report['end_date']
        filing_date = None
        if 'filing_date' in report:
            filing_date = report['filing_date']

        balance_sheet = report['financials']['balance_sheet']
        income_statement = report['financials']['income_statement']
        cash_flow_statement = report['financials']['cash_flow_statement']

        cursor.execute('INSERT OR REPLACE INTO balance_sheet VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (
            cik, company_name, end_date, filing_date,
            None,
            None,
            balance_sheet['current_liabilities']['value'],
            balance_sheet['equity']['value'],
            balance_sheet['equity_attributable_to_noncontrolling_interest']['value'],
            balance_sheet['equity_attributable_to_parent']['value'],
            balance_sheet['liabilities']['value'],
        ))
        cursor.execute('INSERT OR REPLACE INTO income_statement VALUES(?, ?, ?, ?)', (
            cik, company_name, end_date, filing_date
        ))
        cursor.execute('INSERT OR REPLACE INTO cash_flow_statement VALUES(?, ?, ?, ?)', (
            cik, company_name, end_date, filing_date
        ))
    conn.commit()
    conn.close()

def read_database_from_paid_api():
    queries = {
        "DATABASE: balance_sheet": SQL_QUERY_READ_ALL_BALANCE_SHEET,
        "DATABASE: income_statement": SQL_QUERY_READ_ALL_INCOME_STATEMENT,
        "DATABASE: cash_flow_statement": SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT
    }
    with sl.connect(PAID_API_DATABASE) as con:
        cursor = con.cursor()
        for label, query in queries.items():
            print(label)
            cursor.execute(query)
            headers = [description[0] for description in cursor.description]
            print(headers)
            for row in cursor.fetchall():
                print(row)

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
    # Todo: how to automate this process? To fetch financial reports automatically (when the new ones are released),
    # to fetch more historical reports for better testing, to fetch more companies without manual work.
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
        with sl.connect(DATABASE_PATH) as con:
            con.execute(sql_query, data)
            con.commit()
    except Exception as e:
        print(f"Error in save_fetched_data_into_database: {e}")

def _read_all_data_from_database():
    queries = {
        "DATABASE: FINANCIALS": SQL_QUERY_READ_ALL_FINANCIALS,
        "DATABASE: SHARE_PRICES": SQL_QUERY_READ_ALL_SHARE_PRICES
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
