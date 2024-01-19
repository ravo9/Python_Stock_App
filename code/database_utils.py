import sqlite3 as sl

DATABASE_PATH = "../database.db"
SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT = '''CREATE TABLE IF NOT EXISTS cash_flow_statement (company_name TEXT, end_date TEXT, filing_date TEXT, net_cash_flow REAL, PRIMARY KEY (company_name, end_date))'''
SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT = 'SELECT * FROM cash_flow_statement'
SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS = 'SELECT * FROM cash_flow_statement WHERE company_name = ? AND filing_date <= ? ORDER BY filing_date DESC LIMIT ?'

def save_financial_data(data_with_company_ticker):
    _initialize_database()
    with sl.connect(DATABASE_PATH) as con:
        for financial_data, ticker in data_with_company_ticker:
            for report in financial_data['results']:
                cash_flow_statement = report.get('financials', {}).get('cash_flow_statement', {})
                if 'filing_date' not in report or 'value' not in cash_flow_statement.get('net_cash_flow', {}):
                    print(f"Missing data for report {ticker}. Skipping database save.") # add optional filing_date - if not null
                    continue
                try: con.execute('INSERT OR REPLACE INTO cash_flow_statement VALUES (?, ?, ?, ?)', (
                    ticker, report['end_date'], report['filing_date'], cash_flow_statement['net_cash_flow']['value']
                ))
                except Exception as e: print(f"Error in save_fetched_data_into_database: {e}")

def _initialize_database():
    with sl.connect(DATABASE_PATH) as con: con.execute(SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT)

def retrieve_related_financial_reports(number_of_periods, company_ticker, date):
    with sl.connect(DATABASE_PATH) as con:
        recent_reports = con.execute(SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS, (company_ticker, date, number_of_periods)).fetchall()
    if not recent_reports: raise ValueError("ERROR: Empty list")
    return recent_reports

def read_all_data_from_database():
    with sl.connect(DATABASE_PATH) as con:
        cursor = con.execute(SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT)
        print("TABLE: cash_flow_statement")
        print([description[0] for description in cursor.description]) # Headers
        for row in cursor: print(row)
