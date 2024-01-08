# SQL queries:

SQL_QUERY_CREATE_TABLE_INCOME_STATEMENTS = """CREATE TABLE IF NOT EXISTS INCOME_STATEMENT (ticker TEXT, currency TEXT, filling_date DATE, eps FLOAT, epsDiluted FLOAT, PRIMARY KEY (ticker, filling_date));"""
SQL_QUERY_CREATE_TABLE_COMPANY_OUTLOOK = """CREATE TABLE IF NOT EXISTS COMPANY_OUTLOOK (ticker TEXT, filling_date DATE, currency TEXT, freeCashFlow FLOAT, amountOfShares INT, PRIMARY KEY (ticker, filling_date));"""
SQL_QUERY_CREATE_TABLE_SHARE_PRICES = """CREATE TABLE IF NOT EXISTS SHARE_PRICES (ticker TEXT, date DATE, currency TEXT, price FLOAT, PRIMARY KEY (ticker, date));"""
SQL_QUERY_SAVE_INCOME_STATEMENTS = 'INSERT INTO INCOME_STATEMENT (ticker, currency, filling_date, eps, epsDiluted) values(?, ?, ?, ?, ?)'
SQL_QUERY_SAVE_COMPANY_OUTLOOK = 'INSERT INTO COMPANY_OUTLOOK (ticker, filling_date, currency, freeCashFlow, amountOfShares) values(?, ?, ?, ?, ?)'
SQL_QUERY_SAVE_SHARE_PRICES = 'INSERT INTO SHARE_PRICES (ticker, date, currency, price) values(?, ?, ?, ?)'
SQL_QUERY_READ_ALL_INCOME_STATEMENTS = 'SELECT * FROM INCOME_STATEMENT'
SQL_QUERY_READ_ALL_COMPANY_OUTLOOK = 'SELECT * FROM COMPANY_OUTLOOK'
SQL_QUERY_READ_ALL_SHARE_PRICES = 'SELECT * FROM SHARE_PRICES'

# Other constants:
DATE_FORMAT = "%Y-%m-%d"
OUTPUT_DIRECTORY = "results_output/"
GOOGLE_SPREADSHEET_DATA_FILE = "./Stock Historical Data - Sheet1.csv"

# Companies sets:

COMPANIES_TICKERS_TESLA_DISNEY_META = [
    'TSLA',
    'DIS',
    'META'
]

COMPANIES_TICKERS_MULTISET = [
    'AAPL',
    'AMZN',
    'BAC',
    'CRM',
    'DIS',

    'FB',
    'FDX',
    'GOOGL',
    'IBM',
    'KO',

    'MCD',
    'MSFT',
    'NFLX',
    'NKE',
    'NVDA',

    'PYPL',
    'SQ',
    'VZ',
    'WMT',
    'XOM'
]
