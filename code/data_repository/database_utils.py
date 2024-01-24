import sqlite3 as sl

SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT = '''CREATE TABLE IF NOT EXISTS cash_flow_statement (company_name TEXT, date TEXT, net_cash_flow REAL, PRIMARY KEY (company_name, date))'''
SQL_QUERY_CREATE_TABLE_SHARES_AMOUNT = '''CREATE TABLE IF NOT EXISTS SHARES_AMOUNT (ticker TEXT, date TEXT, shares_amount REAL, PRIMARY KEY (ticker, date))'''
SQL_QUERY_CREATE_TABLE_SHARE_PRICE = '''CREATE TABLE IF NOT EXISTS SHARE_PRICE (ticker TEXT, date TEXT, share_price REAL, PRIMARY KEY (ticker, date))'''
SQL_QUERY_CREATE_TABLE_SHARE_PRICES_IN_PERIOD = '''CREATE TABLE IF NOT EXISTS SHARE_PRICES_IN_PERIOD (ticker TEXT, start_date TEXT, end_date TEXT, data TEXT, PRIMARY KEY (ticker, start_date, end_date))'''
SQL_QUERY_EXISTING_REPORTS = "SELECT * FROM cash_flow_statement WHERE company_name = ?"
SQL_QUERY_EXISTING_SHARES_AMOUNT = "SELECT shares_amount FROM SHARES_AMOUNT WHERE ticker = ? AND date = ?"
SQL_QUERY_EXISTING_SHARE_PRICE = "SELECT share_price FROM SHARE_PRICE WHERE ticker = ? AND date = ?"
SQL_QUERY_EXISTING_SHARE_PRICES_IN_PERIOD = "SELECT data FROM SHARE_PRICES_IN_PERIOD WHERE ticker = ? AND start_date = ? AND end_date = ?"
SQL_QUERY_INSERT_FINANCIAL_REPORT = 'INSERT OR REPLACE INTO cash_flow_statement VALUES (?, ?, ?)'
SQL_QUERY_INSERT_SHARES_AMOUNT = 'INSERT OR REPLACE INTO SHARES_AMOUNT VALUES (?, ?, ?)'
SQL_QUERY_INSERT_SHARE_PRICE = 'INSERT OR REPLACE INTO SHARE_PRICE VALUES (?, ?, ?)'
SQL_QUERY_INSERT_SHARE_PRICE_PERIOD = 'INSERT OR REPLACE INTO SHARE_PRICES_IN_PERIOD VALUES (?, ?, ?, ?)'
SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS = 'SELECT * FROM cash_flow_statement WHERE company_name = ? AND date <= ? ORDER BY date DESC LIMIT ?'
SQL_READING_ALL_QUERIES = {'SELECT * FROM cash_flow_statement', 'SELECT * FROM SHARES_AMOUNT', 'SELECT * FROM SHARE_PRICE', 'SELECT * FROM SHARE_PRICES_IN_PERIOD'}
DATABASE_PATH = "../database.db"

def _initialize_database(sql_query):
    with sl.connect(DATABASE_PATH) as con: con.execute(sql_query)

def save_financial_data(financial_data, ticker):
    for report in financial_data:
        date = report['filing_date'] if 'filing_date' in report else report['date']
        save_data_to_database(SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT, SQL_QUERY_INSERT_FINANCIAL_REPORT, ticker, date, report['freeCashFlow'])

def save_data_to_database(init_query, insert_query, *params):
    _initialize_database(init_query)
    with sl.connect(DATABASE_PATH) as con:
        try: con.execute(insert_query, params)
        except Exception as e: print(f"Error in save_data_to_database: {e}")

def get_stored_financial_reports_if_available(number_of_reports_for_calculations, number_of_reports_to_fetch, ticker, date):
    with sl.connect(DATABASE_PATH) as con:
        are_reports_stored = False
        try: are_reports_stored = len(con.execute(SQL_QUERY_EXISTING_REPORTS, (ticker,)).fetchall()) > 0
        # are_reports_stored = len(existing_reports) >= number_of_reports_to_fetch
        except Exception as e: return None
        if are_reports_stored:
            try:
                reports = con.execute(SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS, (ticker, date, number_of_reports_for_calculations)).fetchall()
                if not reports: raise ValueError("ERROR: Empty list")
                # print("RETRIEVED REPORTS FOR " + ticker + " : " + str(len(reports)))
                return reports
            except Exception as e: print(f"Error get_stored_financial_reports_if_available: Request failed: {ticker} - {e}")
        return None

def get_stored_reports_raw(ticker, date, number_of_reports_for_calculations):
    with sl.connect(DATABASE_PATH) as con:
        return con.execute(SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS, (ticker, date, number_of_reports_for_calculations)).fetchall()

def get_stored_value_if_available(query, *params):
    with sl.connect(DATABASE_PATH) as con:
        try: stored_value = con.execute(query, params).fetchall()
        except Exception as e: return None
        return stored_value[0][0] if stored_value and len(stored_value) > 0 and len(stored_value[0]) > 0 else None

def read_all_data_from_database():
    for query in SQL_READING_ALL_QUERIES:
        acc = 0
        with sl.connect(DATABASE_PATH) as con:
            cursor = con.execute(query)
            print([description[0] for description in cursor.description]) # Headers
            for row in cursor: acc += 1 # print(row)
        print("Amount of elements: " + str(acc))
