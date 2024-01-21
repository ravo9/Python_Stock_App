import sqlite3 as sl

DATABASE_PATH = "../database.db"

SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT = '''CREATE TABLE IF NOT EXISTS cash_flow_statement (company_name TEXT, end_date TEXT, filing_date TEXT, net_cash_flow REAL, PRIMARY KEY (company_name, end_date))'''
SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT = 'SELECT * FROM cash_flow_statement'
SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS = 'SELECT * FROM cash_flow_statement WHERE company_name = ? AND filing_date <= ? ORDER BY filing_date DESC LIMIT ?'
SQL_QUERY_EXISTING_REPORTS = "SELECT * FROM cash_flow_statement WHERE company_name = ?"

SQL_QUERY_CREATE_TABLE_SHARES_AMOUNT = '''CREATE TABLE IF NOT EXISTS SHARES_AMOUNT (company_ticker TEXT, date TEXT, shares_amount REAL, PRIMARY KEY (company_ticker, date))'''
SQL_QUERY_READ_ALL_SHARES_AMOUNT = 'SELECT * FROM SHARES_AMOUNT'
SQL_QUERY_EXISTING_SHARES_AMOUNT = "SELECT shares_amount FROM SHARES_AMOUNT WHERE company_ticker = ? AND date = ?"

SQL_QUERY_CREATE_TABLE_SHARE_PRICE = '''CREATE TABLE IF NOT EXISTS SHARE_PRICE (company_ticker TEXT, date TEXT, share_price REAL, PRIMARY KEY (company_ticker, date))'''
SQL_QUERY_READ_ALL_SHARE_PRICE = 'SELECT * FROM SHARE_PRICE'
SQL_QUERY_EXISTING_SHARE_PRICE = "SELECT share_price FROM SHARE_PRICE WHERE company_ticker = ? AND date = ?"

SQL_QUERY_CREATE_TABLE_SHARE_PRICES_IN_PERIOD = '''CREATE TABLE IF NOT EXISTS SHARE_PRICES_IN_PERIOD (company_ticker TEXT, start_date TEXT, end_date TEXT, data TEXT, PRIMARY KEY (company_ticker, start_date, end_date))'''
SQL_QUERY_READ_ALL_SHARE_PRICES_IN_PERIOD = 'SELECT * FROM SHARE_PRICES_IN_PERIOD'
SQL_QUERY_EXISTING_SHARE_PRICES_IN_PERIOD = "SELECT data FROM SHARE_PRICES_IN_PERIOD WHERE company_ticker = ? AND start_date = ? AND end_date = ?"

def _initialize_database(sql_query):
    with sl.connect(DATABASE_PATH) as con: con.execute(sql_query)

# Todo: refactor
def save_financial_data(data_with_company_ticker):
    _initialize_database(SQL_QUERY_CREATE_TABLE_CASH_FLOW_STATEMENT)
    with sl.connect(DATABASE_PATH) as con:
        for financial_data, ticker in data_with_company_ticker:
            for report in financial_data['results']:
                cash_flow_statement = report.get('financials', {}).get('cash_flow_statement', {})
                if 'filing_date' not in report or 'value' not in cash_flow_statement.get('net_cash_flow', {}):
                    # print(f"Missing data for report {ticker}. Skipping database save.") # add optional filing_date - if not null
                    continue
                try: con.execute('INSERT OR REPLACE INTO cash_flow_statement VALUES (?, ?, ?, ?)', (
                    ticker, report['end_date'], report['filing_date'], cash_flow_statement['net_cash_flow']['value']
                ))
                except Exception as e: print(f"Error in save_financial_data: {e}")

def save_shares_amount_data(value, company, date):
    _initialize_database(SQL_QUERY_CREATE_TABLE_SHARES_AMOUNT)
    with sl.connect(DATABASE_PATH) as con:
        try: con.execute('INSERT OR REPLACE INTO SHARES_AMOUNT VALUES (?, ?, ?)', (
            company, date, int(value)
        ))
        except Exception as e: print(f"Error in save_shares_amount_data: {e}")

def save_share_price_daily_data(value, company, date):
    _initialize_database(SQL_QUERY_CREATE_TABLE_SHARE_PRICE)
    with sl.connect(DATABASE_PATH) as con:
        try: con.execute('INSERT OR REPLACE INTO SHARE_PRICE VALUES (?, ?, ?)', (
            company, date, float(value)
        ))
        except Exception as e: print(f"Error in save_share_price_daily_data: {e}")

def save_share_prices_in_period_data(company, start_date, end_date, data):
    _initialize_database(SQL_QUERY_CREATE_TABLE_SHARE_PRICES_IN_PERIOD)
    with sl.connect(DATABASE_PATH) as con:
        try: con.execute('INSERT OR REPLACE INTO SHARE_PRICES_IN_PERIOD VALUES (?, ?, ?, ?)', (
            company, start_date, end_date, data
        ))
        except Exception as e: print(f"Error in save_share_price_daily_data: {e}")

# Todo: refactor
def check_if_these_reports_are_already_stored(company, number_of_reports_intended_to_be_fetched):
    with sl.connect(DATABASE_PATH) as con:
        existing_reports = con.execute(SQL_QUERY_EXISTING_REPORTS, (company,)).fetchall()
        return len(existing_reports) >= number_of_reports_intended_to_be_fetched

def retrieve_related_financial_reports(number_of_periods, company_ticker, date):
    with sl.connect(DATABASE_PATH) as con:
        recent_reports = con.execute(SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS, (company_ticker, date, number_of_periods)).fetchall()
    if not recent_reports: raise ValueError("ERROR: Empty list")
    return recent_reports


def get_stored_shares_amount_value_if_available(company, date):
    with sl.connect(DATABASE_PATH) as con:
        try: stored_value = con.execute(SQL_QUERY_EXISTING_SHARES_AMOUNT, (company, date)).fetchall()
        except Exception as e: return None
        if stored_value != None and len(stored_value)>0 and len(stored_value[0])>0:
            return stored_value[0][0]
        else: return None

def get_stored_share_price_value_if_available(company, date):
    with sl.connect(DATABASE_PATH) as con:
        try: stored_value = con.execute(SQL_QUERY_EXISTING_SHARE_PRICE, (company, date)).fetchall()
        except Exception as e: return None
        if stored_value != None and len(stored_value)>0 and len(stored_value[0])>0:
            return stored_value[0][0]
        else: return None

def get_stored_share_prices_in_period_if_available(company, start_date, end_date):
    with sl.connect(DATABASE_PATH) as con:
        try: stored_value = con.execute(SQL_QUERY_EXISTING_SHARE_PRICES_IN_PERIOD, (company, start_date, end_date)).fetchall()
        except Exception as e: return None
        if stored_value != None and len(stored_value)>0 and len(stored_value[0])>0:
            return stored_value[0][0]
        else: return None

# def read_all_data_from_database():
#     queries = {
#         SQL_QUERY_READ_ALL_CASH_FLOW_STATEMENT,
#         SQL_QUERY_READ_ALL_SHARES_AMOUNT,
#         SQL_QUERY_READ_ALL_SHARE_PRICE,
#         SQL_QUERY_READ_ALL_SHARE_PRICES_IN_PERIOD
#     }
#     for query in queries:
#         with sl.connect(DATABASE_PATH) as con:
#             cursor = con.execute(query)
#             # print("TABLE: cash_flow_statement")
#             print([description[0] for description in cursor.description]) # Headers
#             for row in cursor: print(row)
