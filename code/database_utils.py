import sqlite3 as sl

SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT = '''CREATE TABLE IF NOT EXISTS cash_flow_statement (company_name TEXT, date TEXT, net_cash_flow REAL, PRIMARY KEY (company_name, date))'''
SQL_QUERY_CREATE_TABLE_SHARES_AMOUNT = '''CREATE TABLE IF NOT EXISTS SHARES_AMOUNT (company_ticker TEXT, date TEXT, shares_amount REAL, PRIMARY KEY (company_ticker, date))'''
SQL_QUERY_CREATE_TABLE_SHARE_PRICE = '''CREATE TABLE IF NOT EXISTS SHARE_PRICE (company_ticker TEXT, date TEXT, share_price REAL, PRIMARY KEY (company_ticker, date))'''
SQL_QUERY_CREATE_TABLE_SHARE_PRICES_IN_PERIOD = '''CREATE TABLE IF NOT EXISTS SHARE_PRICES_IN_PERIOD (company_ticker TEXT, start_date TEXT, end_date TEXT, data TEXT, PRIMARY KEY (company_ticker, start_date, end_date))'''
SQL_QUERY_EXISTING_REPORTS = "SELECT * FROM cash_flow_statement WHERE company_name = ?"
SQL_QUERY_EXISTING_SHARES_AMOUNT = "SELECT shares_amount FROM SHARES_AMOUNT WHERE company_ticker = ? AND date = ?"
SQL_QUERY_EXISTING_SHARE_PRICE = "SELECT share_price FROM SHARE_PRICE WHERE company_ticker = ? AND date = ?"
SQL_QUERY_EXISTING_SHARE_PRICES_IN_PERIOD = "SELECT data FROM SHARE_PRICES_IN_PERIOD WHERE company_ticker = ? AND start_date = ? AND end_date = ?"
SQL_QUERY_INSERT_FINANCIAL_REPORT = 'INSERT OR REPLACE INTO cash_flow_statement VALUES (?, ?, ?)'
SQL_QUERY_INSERT_SHARES_AMOUNT = 'INSERT OR REPLACE INTO SHARES_AMOUNT VALUES (?, ?, ?)'
SQL_QUERY_INSERT_SHARE_PRICE = 'INSERT OR REPLACE INTO SHARE_PRICE VALUES (?, ?, ?)'
SQL_QUERY_INSERT_SHARE_PRICE_PERIOD = 'INSERT OR REPLACE INTO SHARE_PRICES_IN_PERIOD VALUES (?, ?, ?, ?)'
SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS = 'SELECT * FROM cash_flow_statement WHERE company_name = ? AND date <= ? ORDER BY date DESC LIMIT ?'
SQL_READING_ALL_QUERIES = {
    'SELECT * FROM cash_flow_statement',
    'SELECT * FROM SHARES_AMOUNT',
    'SELECT * FROM SHARE_PRICE',
    'SELECT * FROM SHARE_PRICES_IN_PERIOD'
}
DATABASE_PATH = "../database.db"

def _initialize_database(sql_query):
    with sl.connect(DATABASE_PATH) as con: con.execute(sql_query)

def save_financial_data(financial_data, ticker):
    for report in financial_data:
        date = report['filing_date'] if 'filing_date' in report else report['date']
        value = report['freeCashFlow']
        _save_data_to_database(SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT, SQL_QUERY_INSERT_FINANCIAL_REPORT, value, ticker, date)

def save_shares_amount_data(value, company, date):
    _save_data_to_database(SQL_QUERY_CREATE_TABLE_SHARES_AMOUNT, SQL_QUERY_INSERT_SHARES_AMOUNT, int(value), company, date)

def save_share_price_daily_data(value, company, date):
    _save_data_to_database(SQL_QUERY_CREATE_TABLE_SHARE_PRICE, SQL_QUERY_INSERT_SHARE_PRICE, float(value), company, date)

def _save_data_to_database(init_query, insert_query, value, company, date):
    _initialize_database(init_query)
    with sl.connect(DATABASE_PATH) as con:
        try: con.execute(insert_query, (company, date, value))
        except Exception as e: print(f"Error in _save_data_to_database: {e}")

def save_share_prices_in_period_data(company, start_date, end_date, data):
    _initialize_database(SQL_QUERY_CREATE_TABLE_SHARE_PRICES_IN_PERIOD)
    with sl.connect(DATABASE_PATH) as con:
        try: con.execute(SQL_QUERY_INSERT_SHARE_PRICE_PERIOD, (company, start_date, end_date, data))
        except Exception as e: print(f"Error in save_share_price_daily_data: {e}")

def get_stored_financial_reports_if_available(number_of_reports_for_calculations, number_of_reports_to_fetch, company_ticker, date):
    with sl.connect(DATABASE_PATH) as con:
        are_reports_stored = False
        try:
            existing_reports = con.execute(SQL_QUERY_EXISTING_REPORTS, (company_ticker,)).fetchall()
            # are_reports_stored = len(existing_reports) >= number_of_reports_to_fetch
            are_reports_stored = len(existing_reports) > 0
        except Exception as e: return None
        if are_reports_stored:
            try:
                recent_reports = con.execute(SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS, (
                    company_ticker, date, number_of_reports_for_calculations
                )).fetchall()
                if not recent_reports: raise ValueError("ERROR: Empty list")
                return recent_reports
            except Exception as e: print(f"Request failed: {company_ticker} - {e}")
        return None

def get_stored_shares_amount_value_if_available(company, date):
    return _get_stored_value_if_available(SQL_QUERY_EXISTING_SHARES_AMOUNT, company, date)

def get_stored_share_price_value_if_available(company, date):
    return _get_stored_value_if_available(SQL_QUERY_EXISTING_SHARE_PRICE, company, date)

def _get_stored_value_if_available(query, company, date):
    with sl.connect(DATABASE_PATH) as con:
        try: stored_value = con.execute(query, (company, date)).fetchall()
        except Exception as e: return None
        if stored_value != None and len(stored_value)>0 and len(stored_value[0])>0: return stored_value[0][0]
        else: return None

def get_stored_share_prices_in_period_if_available(company, start_date, end_date):
    with sl.connect(DATABASE_PATH) as con:
        try: stored_value = con.execute(SQL_QUERY_EXISTING_SHARE_PRICES_IN_PERIOD, (company, start_date, end_date)).fetchall()
        except Exception as e: return None
        if stored_value != None and len(stored_value)>0 and len(stored_value[0])>0: return stored_value[0][0]
        else: return None

def read_all_data_from_database():
    for query in SQL_READING_ALL_QUERIES:
        acc = 0
        with sl.connect(DATABASE_PATH) as con:
            cursor = con.execute(query)
            print([description[0] for description in cursor.description]) # Headers
            for row in cursor:
                # print(row)
                acc += 1
        print("Amount of elements: " + str(acc))
