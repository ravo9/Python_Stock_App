import requests
import pandas_datareader as web
import pandas
import json
from PrintingUtils import printApiDataFetched


# 7 years
DATA_FETCHING_FINANCIAL_MODELLING_API_KEY = 'ee22bac37cfc64407760039b37d56065'
DATA_FETCHING_INCOME_STATEMENT_AMOUNT_OF_REPORTS = 28
DATA_FETCHING_INCOME_STATEMENT_PERIOD = 'quarter'

DATA_FETCHING_INCOME_STATEMENT_ENDPOINT_URL = "https://financialmodelingprep.com/api/v3/income-statement/"
DATA_FETCHING_COMPANY_OUTLOOK_ENDPOINT_URL = "https://financialmodelingprep.com/api/v4/company-outlook/"


def fetchDataFromApi(url, params, debugMode = False):
    resp = requests.get(url=url, params=params)
    data = resp.json()
    printApiDataFetched(data, debugMode)
    return data


def fetchCompanyOutlookFromTheApi(companies):
    apiKey = DATA_FETCHING_FINANCIAL_MODELLING_API_KEY
    allCompaniesData = []

    for company in companies:
        url = DATA_FETCHING_COMPANY_OUTLOOK_ENDPOINT_URL
        params = dict(
            symbol=company,
            apikey=apiKey
            )

        data = fetchDataFromApi(url, params, False)
        data_correcctedQuotemarks = json.dumps(data)
        jsonData = json.loads(str(data_correcctedQuotemarks))
        jsonData_financialsQuarter = jsonData["financialsQuarter"]

        jsonData_cash = jsonData_financialsQuarter["cash"]
        jsonData_income = jsonData_financialsQuarter["income"]

        amountOfReportedQuarters = len(jsonData_cash)
        if (len(jsonData_cash) != len(jsonData_income)):
            print("ERROR: Incorrect reports number!")
            return null

        for i in range(amountOfReportedQuarters):
            ticker = jsonData_cash[i]["symbol"]
            if (jsonData_income[i]["fillingDate"] != jsonData_cash[i]["fillingDate"]):
                print("ERROR: Incorrect reports dates!")
                return null
            # Filling date seems to be okay as according to stackexchange.com it's the date when the report is published.
            fillingDate = jsonData_cash[i]["fillingDate"]
            currency = jsonData_cash[i]["reportedCurrency"]
            freeCashFlow = jsonData_cash[i]["freeCashFlow"]
            # Todo: Is it a good one? We should rather have amountOfShares from the same day as the share price.
            amountOfShares = jsonData_income[i]["weightedAverageShsOut"]

            row = [ticker, fillingDate, currency, freeCashFlow, amountOfShares]
            allCompaniesData.append(row)

    return allCompaniesData


def fetchIncomeStatementsFromTheApi(companies):
    period = DATA_FETCHING_INCOME_STATEMENT_PERIOD
    limit = DATA_FETCHING_INCOME_STATEMENT_AMOUNT_OF_REPORTS
    apiKey = DATA_FETCHING_FINANCIAL_MODELLING_API_KEY

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
