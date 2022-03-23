import requests
import pandas_datareader as web
import pandas
import json
from printing_utils import print_api_data_fetched


# 7 years
DATA_FETCHING_FINANCIAL_MODELLING_API_KEY = 'ee22bac37cfc64407760039b37d56065'
DATA_FETCHING_INCOME_STATEMENT_AMOUNT_OF_REPORTS = 28
DATA_FETCHING_INCOME_STATEMENT_PERIOD = 'quarter'

DATA_FETCHING_INCOME_STATEMENT_ENDPOINT_URL = "https://financialmodelingprep.com/api/v3/income-statement/"
DATA_FETCHING_COMPANY_OUTLOOK_ENDPOINT_URL = "https://financialmodelingprep.com/api/v4/company-outlook/"


def fetch_data_from_api(url, params, debug_mode = False):
    resp = requests.get(url=url, params=params)
    data = resp.json()
    print_api_data_fetched(data, debug_mode)
    return data


def fetch_company_outlook_from_the_api(companies):
    api_key = DATA_FETCHING_FINANCIAL_MODELLING_API_KEY
    all_companies_data = []

    for company in companies:
        url = DATA_FETCHING_COMPANY_OUTLOOK_ENDPOINT_URL
        params = dict(
            symbol=company,
            apikey=api_key
            )

        data = fetch_data_from_api(url, params, False)
        data_correccted_quotemarks = json.dumps(data)
        json_data = json.loads(str(data_correccted_quotemarks))
        json_data_financials_quarter = json_data["financialsQuarter"]

        json_data_cash = json_data_financials_quarter["cash"]
        json_data_income = json_data_financials_quarter["income"]

        amount_of_reported_quarters = len(json_data_cash)
        if len(json_data_cash) != len(json_data_income):
            print("ERROR: Incorrect reports number!")
            return None

        for i in range(amount_of_reported_quarters):
            ticker = json_data_cash[i]["symbol"]
            if json_data_income[i]["fillingDate"] != json_data_cash[i]["fillingDate"]:
                print("ERROR: Incorrect reports dates!")
                print(json_data_income[i]["fillingDate"])
                print(json_data_cash[i]["fillingDate"])
                return None
            # Filling date seems to be okay as according to stackexchange.com it's the date when the report is published.
            filling_date = json_data_cash[i]["fillingDate"]
            currency = json_data_cash[i]["reportedCurrency"]
            free_cash_flow = json_data_cash[i]["freeCashFlow"]
            # Todo: Is it a good one? We should rather have amountOfShares from the same day as the share price.
            amount_of_shares = json_data_income[i]["weightedAverageShsOut"]

            row = [ticker, filling_date, currency, free_cash_flow, amount_of_shares]
            all_companies_data.append(row)

    return all_companies_data


def fetch_income_statements_from_the_api(companies):
    period = DATA_FETCHING_INCOME_STATEMENT_PERIOD
    limit = DATA_FETCHING_INCOME_STATEMENT_AMOUNT_OF_REPORTS
    api_key = DATA_FETCHING_FINANCIAL_MODELLING_API_KEY

    all_companies_data = []
    for company in companies:
        url = DATA_FETCHING_INCOME_STATEMENT_ENDPOINT_URL + company
        params = dict(
            period=period,
            limit=limit,
            apikey=api_key
            )
        data = fetch_data_from_api(url, params, False)
        for row in data:
            all_companies_data.append(row)
    return all_companies_data


def fetch_share_prices_from_the_api(companies, start_date, end_date):
    dataframes = []
    for company in companies:
        share_prices_table = web.DataReader(company, data_source='yahoo', start=start_date, end=end_date)
        values = share_prices_table.filter(["High", "Low"])
        values = values.assign(Ticker=company)
        dataframes.append(values)
    return pandas.concat(dataframes)
