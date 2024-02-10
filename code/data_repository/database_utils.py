import sqlite3 as sl

SQL_CREATE_CASH_FLOW_STATEMENT = '''CREATE TABLE IF NOT EXISTS cash_flow_statement (company_name TEXT, date TEXT, net_cash_flow REAL, PRIMARY KEY (company_name, date))'''
SQL_CREATE_INCOME_STATEMENT = '''CREATE TABLE IF NOT EXISTS income_statement (company_name TEXT, date TEXT, interest_expense REAL, PRIMARY KEY (company_name, date))'''
SQL_CREATE_BALANCE_SHEET = '''CREATE TABLE IF NOT EXISTS balance_sheet (company_name TEXT, date TEXT, total_debt REAL, PRIMARY KEY (company_name, date))'''
SQL_CREATE_SHARES_AMOUNT = '''CREATE TABLE IF NOT EXISTS SHARES_AMOUNT (ticker TEXT, date TEXT, shares_amount REAL, PRIMARY KEY (ticker, date))'''
SQL_CREATE_SHARE_PRICE = '''CREATE TABLE IF NOT EXISTS SHARE_PRICE (ticker TEXT, date TEXT, share_price REAL, PRIMARY KEY (ticker, date))'''
SQL_CREATE_SHARE_PRICES_IN_PERIOD = '''CREATE TABLE IF NOT EXISTS SHARE_PRICES_IN_PERIOD (ticker TEXT, start_date TEXT, end_date TEXT, data TEXT, PRIMARY KEY (ticker, start_date, end_date))'''
SQL_EXISTING_CASH_FLOW_STATEMENTS = "SELECT * FROM cash_flow_statement WHERE company_name = ?"
SQL_EXISTING_INCOME_STATEMENTS = "SELECT * FROM income_statement WHERE company_name = ?"
SQL_EXISTING_BALANCE_SHEETS = "SELECT * FROM balance_sheet WHERE company_name = ?"
SQL_EXISTING_SHARES_AMOUNT = "SELECT shares_amount FROM SHARES_AMOUNT WHERE ticker = ? AND date = ?"
SQL_EXISTING_SHARE_PRICE = "SELECT share_price FROM SHARE_PRICE WHERE ticker = ? AND date = ?"
SQL_EXISTING_SHARE_PRICES_IN_PERIOD = "SELECT data FROM SHARE_PRICES_IN_PERIOD WHERE ticker = ? AND start_date = ? AND end_date = ?"
SQL_INSERT_CASH_FLOW_STATEMENT = 'INSERT OR REPLACE INTO cash_flow_statement VALUES (?, ?, ?)'
SQL_INSERT_INCOME_STATEMENT = 'INSERT OR REPLACE INTO income_statement VALUES (?, ?, ?)'
SQL_INSERT_BALANCE_SHEET = 'INSERT OR REPLACE INTO balance_sheet VALUES (?, ?, ?)'
SQL_INSERT_SHARES_AMOUNT = 'INSERT OR REPLACE INTO SHARES_AMOUNT VALUES (?, ?, ?)'
SQL_INSERT_SHARE_PRICE = 'INSERT OR REPLACE INTO SHARE_PRICE VALUES (?, ?, ?)'
SQL_INSERT_SHARE_PRICE_PERIOD = 'INSERT OR REPLACE INTO SHARE_PRICES_IN_PERIOD VALUES (?, ?, ?, ?)'
SQL_MOST_RECENT_CASH_FLOW_STATEMENTS = 'SELECT * FROM cash_flow_statement WHERE company_name = ? AND date <= ? ORDER BY date DESC LIMIT ?'
SQL_MOST_RECENT_INCOME_STATEMENTS = 'SELECT * FROM income_statement WHERE company_name = ? AND date <= ? ORDER BY date DESC LIMIT ?'
SQL_MOST_RECENT_BALANCE_SHEETS = 'SELECT * FROM balance_sheet WHERE company_name = ? AND date <= ? ORDER BY date DESC LIMIT ?'
SQL_READING_ALL_QUERIES = {'SELECT * FROM cash_flow_statement', 'SELECT * FROM SHARES_AMOUNT', 'SELECT * FROM SHARE_PRICE', 'SELECT * FROM SHARE_PRICES_IN_PERIOD'}
DATABASE_PATH = "../database.db"

def _initialize_database(SQL_):
    with sl.connect(DATABASE_PATH) as con: con.execute(SQL_)

def save_financial_statements_data(statement_type, financial_data, ticker, tested_property='operatingCashFlow'):
    for report in financial_data:
        date = report['filing_date'] if 'filing_date' in report else report['date']
        if statement_type == 'cash_flow_statement': save_data_to_database(SQL_CREATE_CASH_FLOW_STATEMENT, SQL_INSERT_CASH_FLOW_STATEMENT, ticker, date, report[tested_property])
        elif statement_type == 'income_statement': save_data_to_database(SQL_CREATE_INCOME_STATEMENT, SQL_INSERT_INCOME_STATEMENT, ticker, date, report['interestExpense'])
        elif statement_type == 'balance_sheet': save_data_to_database(SQL_CREATE_BALANCE_SHEET, SQL_INSERT_BALANCE_SHEET, ticker, date, report['totalDebt'])

def save_data_to_database(init_query, insert_query, *params):
    _initialize_database(init_query)
    with sl.connect(DATABASE_PATH) as con:
        try: con.execute(insert_query, params)
        except Exception as e: print(f"Error in save_data_to_database: {e}")

def get_stored_financial_statements_if_available(statement_type, number_of_reports_for_calculations, number_of_reports_to_fetch, ticker, date):
    sql_existing_statements = {'cash_flow_statement': SQL_EXISTING_CASH_FLOW_STATEMENTS, 'income_statement': SQL_EXISTING_INCOME_STATEMENTS, 'balance_sheet': SQL_EXISTING_BALANCE_SHEETS}
    sql_recent_statements = {'cash_flow_statement': SQL_MOST_RECENT_CASH_FLOW_STATEMENTS,'income_statement': SQL_MOST_RECENT_INCOME_STATEMENTS, 'balance_sheet': SQL_MOST_RECENT_BALANCE_SHEETS}
    with sl.connect(DATABASE_PATH) as con:
        try:
            are_reports_stored = len(con.execute(sql_existing_statements[statement_type], (ticker,)).fetchall()) > 0
            # are_reports_stored = len(existing_reports) >= number_of_reports_to_fetch
            if are_reports_stored:
                reports = con.execute(sql_recent_statements[statement_type], (ticker, date, number_of_reports_for_calculations)).fetchall()
                if not reports: raise ValueError("ERROR: Empty list")
                if (len(reports) < number_of_reports_for_calculations):
                    print("Error: not enough reports for " + ticker)
                    print("Fetched " + str(len(reports)) + " out of required " + str(number_of_reports_for_calculations))
                return reports
        except Exception as e:
            print(f"Error in get_stored_financial_statements_if_available {statement_type}: Request failed: {ticker} - {e}")
            return None

def get_stored_financial_statements_raw(statement_type, ticker, date, number_of_reports_for_calculations):
    sql_query = ""
    if statement_type == "cash_flow_statement": sql_query = SQL_MOST_RECENT_CASH_FLOW_STATEMENTS
    elif statement_type == "income_statement": sql_query = SQL_MOST_RECENT_INCOME_STATEMENTS
    elif statement_type == "balance_sheet": sql_query = SQL_MOST_RECENT_BALANCE_SHEETS
    with sl.connect(DATABASE_PATH) as con:
        return con.execute(sql_query, (ticker, date, number_of_reports_for_calculations)).fetchall()

# Todo: does it work with [0][0] in all cases?
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
