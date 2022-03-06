import requests
import pandas_datareader as web
import pandas
from PrintingUtils import printApiDataFetched


# 7 years
DATA_FETCHING_INCOME_STATEMENT_AMOUNT_OF_REPORTS = 28
DATA_FETCHING_INCOME_STATEMENT_PERIOD = 'quarter'
DATA_FETCHING_INCOME_STATEMENT_API_KEY = 'ee22bac37cfc64407760039b37d56065'
DATA_FETCHING_INCOME_STATEMENT_ENDPOINT_URL = "https://financialmodelingprep.com/api/v3/income-statement/"


def fetchDataFromApi(url, params, debugMode = False):
    resp = requests.get(url=url, params=params)
    data = resp.json()
    printApiDataFetched(data, debugMode)
    return data


def fetchIncomeStatementsFromTheApi(companies):
    period = DATA_FETCHING_INCOME_STATEMENT_PERIOD
    limit = DATA_FETCHING_INCOME_STATEMENT_AMOUNT_OF_REPORTS
    apiKey = DATA_FETCHING_INCOME_STATEMENT_API_KEY

    allCompaniesData = []
    for company in companies:
        url = DATA_FETCHING_INCOME_STATEMENT_ENDPOINT_URL + company
        params = dict(
            period=period,
            limit=limit,
            apikey=apiKey
            )
        data = fetchDataFromApi(url, params, False)
        for row in data:
            allCompaniesData.append(row)
    return allCompaniesData


def fetchSharePricesFromTheApi(companies, startDate, endDate):
    dataframes = []
    for company in companies:
        sharePricesTable = web.DataReader(company, data_source='yahoo', start=startDate, end=endDate)
        values = sharePricesTable.filter(["High", "Low"])
        values = values.assign(Ticker=company)
        dataframes.append(values)
    return pandas.concat(dataframes)
