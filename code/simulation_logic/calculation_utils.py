import sys
import os
import unittest
from unittest.mock import patch
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database_utils import fetch_price_in_particular_period_dynamically

calculate_change_in_share_price = lambda first_day_price, last_day_price: (last_day_price - first_day_price)/first_day_price

# If we check difference between 01.01.23 and 0.1.01.24, and the last day is not available - then it will actually check 01.01.23 - 29.12.23.
def calculate_average_share_price_change_for_given_companies_in_given_period(companies_tickers, start_date, end_date):
    sum_of_changes = 0.0
    for company in companies_tickers:
        share_prices_table = fetch_price_in_particular_period_dynamically(company, start_date, end_date)
        first_day_price, last_day_price = share_prices_table[0][0], share_prices_table[0][-1]
        sum_of_changes += calculate_change_in_share_price(first_day_price, last_day_price)
    return sum_of_changes / len(companies_tickers)

def calculate_investment_value_change(companies_tickers_with_weights, is_it_last_sub_period, start_date, end_date):
    change_in_invested_money = 0.0
    sum_of_all_bets = sum(weight for _, weight in companies_tickers_with_weights)
    for company_ticker, company_bet_weight in companies_tickers_with_weights:
        share_prices_table = fetch_price_in_particular_period_dynamically(company_ticker, start_date, end_date)
        first_day_price, last_day_price = share_prices_table[0][0], share_prices_table[0][-1]
        change_in_invested_money += calculate_change_in_share_price(first_day_price, last_day_price) * company_bet_weight / sum_of_all_bets
    return change_in_invested_money

# UNIT TESTING

# Todo: fix unit tests

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

    @patch('simulation_logic.calculation_utils.fetch_prices_in_particular_period')
    def test_average_price_increase(self, mock_fetch_prices):
        # Mock data: Prices increase for both companies
        mock_fetch_prices.side_effect = [
            [(100, 110)],  # First company: 10% increase
            [(200, 240)]   # Second company: 20% increase
        ]
        companies = ['COMPANY_A', 'COMPANY_B']
        average_change = calculate_average_share_price_change_for_given_companies_in_given_period(companies, '2021-01-01', '2021-01-31')
        self.assertAlmostEqual(average_change, 0.15, places=2) # Expecting 15% average increase

    @patch('simulation_logic.calculation_utils.fetch_prices_in_particular_period')
    def test_average_price_no_change(self, mock_fetch_prices):
        # Mock data: No price change for both companies
        mock_fetch_prices.side_effect = [
            [(100,), (100,)],  # First company: No change
            [(200,), (200,)]   # Second company: No change
        ]
        companies = ['COMPANY_A', 'COMPANY_B']
        average_change = calculate_average_share_price_change_for_given_companies_in_given_period(companies, '2021-01-01', '2021-01-31')
        self.assertEqual(average_change, 0)  # Expecting 0% change
