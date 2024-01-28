from .database_utils import get_stored_value_if_available, get_stored_financial_statements_if_available, SQL_EXISTING_SHARE_PRICE, SQL_EXISTING_SHARES_AMOUNT, SQL_EXISTING_SHARE_PRICES_IN_PERIOD
from .api_utils import fetch_share_price_daily, fetch_share_prices_per_period, fetch_total_amount_of_shares_on_particular_day, fetch_financial_statements
from datetime import datetime, timedelta
import json
import unittest
from unittest.mock import Mock, patch

DATE_FORMAT = "%Y-%m-%d"

def retrieve_financial_statements(statement_type, number_of_reports_for_calculations, number_of_reports_to_fetch, ticker, date):
    stored_value = get_stored_financial_statements_if_available(statement_type, number_of_reports_for_calculations, number_of_reports_to_fetch, ticker, date)
    return stored_value if stored_value is not None else fetch_financial_statements(statement_type, ticker, number_of_reports_for_calculations, number_of_reports_to_fetch, date)

def retrieve_share_price_daily(company, date, date_format = DATE_FORMAT):
    stored_value = get_stored_value_if_available(SQL_EXISTING_SHARE_PRICE, company, date) # Caching
    if stored_value != None: return stored_value
    return fetch_share_price_daily(company, date, date_format)

def retrieve_share_prices_per_period(company, start_date, end_date, date_format = DATE_FORMAT):
    end_date = (datetime.strptime(end_date, date_format) + timedelta(days=1)).strftime(date_format) # Caching
    stored_value = get_stored_value_if_available(SQL_EXISTING_SHARE_PRICES_IN_PERIOD, company, start_date, end_date)
    if stored_value != None: return json.loads(stored_value)
    return fetch_share_prices_per_period(company, start_date, end_date, date_format)

def retrieve_total_amount_of_shares_on_particular_day(company, date_str):
    # Todo: 1. this is making problems with current date as date - delay around 10 days sometimes 2.optimise (not reason to fetch this whole table).
    date = datetime.strptime(date_str, DATE_FORMAT)
    stored_value = get_stored_value_if_available(SQL_EXISTING_SHARES_AMOUNT, company, date) # Caching
    if stored_value != None: return stored_value  # sometimes was spotted missing in a big dataset (when should've been already cached)
    return fetch_total_amount_of_shares_on_particular_day(company, date)

# UNIT TESTING

class TestRetrieveFinancialReports(unittest.TestCase):

    @patch('data_repository.database_utils.get_stored_financial_statements_if_available')
    @patch('data_repository.api_utils.fetch_financial_statements')
    def test_retrieve_from_fetch(self, mock_fetch, mock_get_stored):
        # Setup
        test_ticker = ['AAPL', 'TSLA']
        test_date = '2024-01-01'
        test_number_of_reports_for_calculations = 8
        test_number_of_reports_to_fetch = 10
        mock_get_stored.return_value = None
        mock_fetch.return_value = []
        # Execute
        results = []
        for ticker in test_ticker:
            results += retrieve_financial_statements("cash_flow_statement", test_number_of_reports_for_calculations, test_number_of_reports_to_fetch, ticker, test_date)
        # Verify
        self.assertEqual(len(results), 16)

class TestRetrieveSharePriceDaily(unittest.TestCase):

    @patch('data_repository.database_utils.get_stored_value_if_available')
    @patch('data_repository.api_utils.fetch_share_price_daily')
    def test_retrieve_share_price_daily(self, mock_fetch, mock_get_stored):
        # Setup
        test_companies = ['AAPL', 'TSLA']
        test_date = '2024-01-02'
        mock_results = [186.17, 247.83]  # Real values for 02.01.24, average from 'High' and 'Low'.
        # Mocking: Return None for the first call (cache miss) and then return the mock result
        mock_get_stored.side_effect = [None, *mock_results]
        mock_fetch.side_effect = mock_results
        # Execute & Verify
        for i, company in enumerate(test_companies):
            result = retrieve_share_price_daily(company, test_date)
            self.assertAlmostEqual(result, mock_results[i], places = 2)

class TestRetrieveTotalAmountOfSharesOnParticularDay(unittest.TestCase):

    @patch('data_repository.database_utils.get_stored_value_if_available')
    @patch('data_repository.api_utils.fetch_total_amount_of_shares_on_particular_day')
    def test_retrieve_total_amount_of_shares(self, mock_fetch, mock_get_stored):
        # Setup
        test_companies = ['AAPL', 'TSLA']
        test_date = '2024-01-01'
        mock_share_amounts = [15552799744, 3186200064]  # Real values for 03/05.01.24 (as it should be picked up for 01.01.24).
        # Mocking: Return None for the first call (cache miss) and then return the mock result
        mock_get_stored.side_effect = [None, *mock_share_amounts]
        mock_fetch.side_effect = mock_share_amounts
        # Execute & Verify
        for i, company in enumerate(test_companies):
            result = retrieve_total_amount_of_shares_on_particular_day(company, test_date)
            self.assertEqual(result, mock_share_amounts[i])
