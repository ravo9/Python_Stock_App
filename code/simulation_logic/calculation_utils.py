import sys
import os
import unittest
from unittest.mock import patch
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from data_repository.data_repository import retrieve_share_price_daily, retrieve_share_prices_per_period, retrieve_total_amount_of_shares_on_particular_day, retrieve_financial_reports
from config import NUMBER_OF_REPORTS_TO_FETCH_FROM_API

calculate_change_in_share_price = lambda first_day_price, last_day_price: (last_day_price - first_day_price)/first_day_price

# If we check difference between 01.01.23 and 0.1.01.24, and the last day is not available - then it will actually check 01.01.23 - 29.12.23.
def calculate_average_share_price_change_for_given_companies_in_given_period(companies_tickers, start_date, end_date):
    sum_of_changes = 0.0
    for company in companies_tickers:
        share_prices_table = retrieve_share_prices_per_period(company, start_date, end_date)
        first_day_price, last_day_price = share_prices_table[0][0], share_prices_table[0][-1]
        sum_of_changes += calculate_change_in_share_price(first_day_price, last_day_price)
    return sum_of_changes / len(companies_tickers)

def calculate_investment_value_change(companies_tickers_with_weights, start_date, end_date):
    change_in_invested_money = 0.0
    sum_of_all_bets = sum(abs(weight) for _, weight in companies_tickers_with_weights)
    for ticker, company_bet_weight in companies_tickers_with_weights:
        share_prices_table = retrieve_share_prices_per_period(ticker, start_date, end_date)
        first_day_price, last_day_price = share_prices_table[0][0], share_prices_table[0][-1]

        if sum_of_all_bets == 0.0:
            change_in_invested_money = 0
        else:
            change_in_invested_money += calculate_change_in_share_price(first_day_price, last_day_price) * company_bet_weight / sum_of_all_bets
    return change_in_invested_money

def calculate_weights(companies, date, number_of_reports_for_calculation, ATTRIBUTE_OF_DECISION_INDEX = 2):
    calculated_weights = []
    sum_of_weights = 0.0
    for ticker in companies:
        financial_reports = retrieve_financial_reports(number_of_reports_for_calculation, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, ticker, date)
        all_shares_amount  = retrieve_total_amount_of_shares_on_particular_day(ticker, date)
        share_price_for_this_date = retrieve_share_price_daily(ticker, date)
        average_real_value_over_analysed_reports = sum(report[ATTRIBUTE_OF_DECISION_INDEX] for report in financial_reports) / len(financial_reports)
        value_per_dollar_spent = average_real_value_over_analysed_reports / all_shares_amount / share_price_for_this_date
        calculated_weights.append((ticker, value_per_dollar_spent))
    return calculated_weights

def find_out_value_per_dollar_spent_today(companies, date, number_of_reports_in_calculations):
    for item in sorted(calculate_weights(companies, date, number_of_reports_in_calculations), key=lambda x: x[1], reverse=True):
        print(item)

# UNIT TESTING

class TestCalculateChangeInSharePrice(unittest.TestCase):

    def test_increase_in_price(self):
        self.assertEqual(calculate_change_in_share_price(100, 110), 0.1)

    def test_decrease_in_price(self):
        self.assertEqual(calculate_change_in_share_price(100, 90), -0.1)

    def test_no_change_in_price(self):
        self.assertEqual(calculate_change_in_share_price(100, 100), 0)

    def test_zero_initial_price(self):
        with self.assertRaises(ZeroDivisionError):
            calculate_change_in_share_price(0, 100)

class TestCalculateAverageSharePriceChange(unittest.TestCase):

    @patch('simulation_logic.calculation_utils.retrieve_share_prices_per_period')
    def test_average_price_increase(self, mock_fetch_prices):
        # Mock data: Prices increase for both companies
        mock_fetch_prices.side_effect = [
            [(100, 110)],  # First company: 10% increase
            [(200, 240)]   # Second company: 20% increase
        ]
        companies = ['COMPANY_A', 'COMPANY_B']
        average_change = calculate_average_share_price_change_for_given_companies_in_given_period(companies, '2021-01-01', '2021-01-31')
        self.assertAlmostEqual(average_change, 0.15, places=2) # Expecting 15% average increase

    @patch('simulation_logic.calculation_utils.retrieve_share_prices_per_period')
    def test_average_price_no_change(self, mock_fetch_prices):
        # Mock data: No price change for both companies
        mock_fetch_prices.side_effect = [
            [(100,), (100,)],  # First company: No change
            [(200,), (200,)]   # Second company: No change
        ]
        companies = ['COMPANY_A', 'COMPANY_B']
        average_change = calculate_average_share_price_change_for_given_companies_in_given_period(companies, '2021-01-01', '2021-01-31')
        self.assertEqual(average_change, 0)  # Expecting 0% change
