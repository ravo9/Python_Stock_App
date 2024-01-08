import pandas
import yfinance as yf

def fetch_share_prices_from_the_api(companies, start_date, end_date):
    dataframes = []
    for company in companies:
        share_prices_table = yf.download(company, start=start_date, end=end_date, progress=False)
        values = share_prices_table.filter(["High", "Low"])
        values = values.assign(Ticker=company)
        dataframes.append(values)
    return pandas.concat(dataframes)
