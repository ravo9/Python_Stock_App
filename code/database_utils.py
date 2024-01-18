from api_utils import fetch_financial_data_for_given_companies
import sqlite3 as sl
import yfinance as yf

SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT = '''CREATE TABLE IF NOT EXISTS cash_flow_statement (company_name TEXT, end_date TEXT, filing_date TEXT, net_cash_flow REAL, PRIMARY KEY (company_name, end_date))'''
SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT = 'SELECT * FROM cash_flow_statement'
SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS = 'SELECT * FROM cash_flow_statement WHERE company_name = ? AND filing_date <= ? ORDER BY filing_date DESC LIMIT ?'

DATABASE_PATH = "../database.db"

def fetch_necessary_data_for_experiment(companies):
    _save_financial_data_in_database(fetch_financial_data_for_given_companies(companies))
    # read_all_data_from_database()

def _save_financial_data_in_database(data_with_company_ticker):
    _initialize_database()
    for financial_data, ticker in data_with_company_ticker:
        for report in financial_data['results']:
            filing_date = report.get('filing_date')
            cash_flow_statement = report.get('financials').get('cash_flow_statement')
            if (cash_flow_statement == None) or (filing_date == None):
                print(f"Missing data for report {ticker, filing_date}. Skipping database save.")
                continue
            try:
                with sl.connect(DATABASE_PATH) as con:
                    con.execute('INSERT OR REPLACE INTO cash_flow_statement VALUES(?, ?, ?, ?)', (
                        ticker, report['end_date'], filing_date, cash_flow_statement['net_cash_flow']['value']
                    ))
                    con.commit()
            except Exception as e:
                print(f"Error in save_fetched_data_into_database: {e}")

def _initialize_database():
    con = sl.connect(DATABASE_PATH)
    with con:
        con.execute(SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT)

def retrieve_related_financial_reports(number_of_periods, company_ticker, date):
    con = sl.connect(DATABASE_PATH)
    with con:
        most_recent_financial_reports_for_this_date = (con.execute(
            SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS, (company_ticker, date, number_of_periods)
        )).fetchall()
    if most_recent_financial_reports_for_this_date == []:
        raise ValueError("ERROR: Empty list")
    return most_recent_financial_reports_for_this_date

def read_all_data_from_database():
    label = "TABLE: cash_flow_statement"
    sql_query = SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT
    with sl.connect(DATABASE_PATH) as con:
        cursor = con.cursor()
        cursor.execute(query)
        print(label)
        headers = [description[0] for description in cursor.description]
        print(headers)
        for row in cursor.fetchall():
            print(row)
