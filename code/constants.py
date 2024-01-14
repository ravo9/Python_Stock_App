# SQL queries:

SQL_QUERY_CREATE_TABLE_FINANCIALS = """CREATE TABLE IF NOT EXISTS FINANCIALS (ticker TEXT, filling_date DATE, currency TEXT, freeCashFlow FLOAT, amountOfShares INT, PRIMARY KEY (ticker, filling_date));"""
SQL_QUERY_CREATE_TABLE_SHARE_PRICES = """CREATE TABLE IF NOT EXISTS SHARE_PRICES (ticker TEXT, date DATE, currency TEXT, price FLOAT, PRIMARY KEY (ticker, date));"""
SQL_QUERY_SAVE_FINANCIALS = 'INSERT OR REPLACE INTO FINANCIALS (ticker, filling_date, currency, freeCashFlow, amountOfShares) values(?, ?, ?, ?, ?)'
SQL_QUERY_SAVE_SHARE_PRICES = 'INSERT OR REPLACE INTO SHARE_PRICES (ticker, date, currency, price) values(?, ?, ?, ?)'
SQL_QUERY_READ_ALL_FINANCIALS = 'SELECT * FROM FINANCIALS'
SQL_QUERY_READ_ALL_SHARE_PRICES = 'SELECT * FROM SHARE_PRICES'
SQL_QUERY_MOST_RECENT_FINANCIAL_REPORTS = 'SELECT * FROM FINANCIALS WHERE ticker = ? AND filling_date <= ? ORDER BY filling_date DESC LIMIT ?'

# Other constants:
DATE_FORMAT = "%Y-%m-%d"
GOOGLE_SPREADSHEET_DATA_FILE = "../Stock Historical Data - Sheet1.csv"
DATABASE_PATH = "./database.db"
