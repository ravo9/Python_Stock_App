import pandas
import yfinance as yf

def fetch_share_prices_from_yahoo_finance_api(companies, start_date, end_date):
    fetched_prices = []
    table_columns_to_be_fetched = ["High", "Low"]
    for company in companies:
        share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
        values = share_prices_table.filter(table_columns_to_be_fetched)
        fetched_prices.append(values.assign(Ticker=company))
    return pandas.concat(fetched_prices)
