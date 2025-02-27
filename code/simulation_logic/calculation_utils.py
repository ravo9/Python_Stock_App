import sys
import os
import unittest
from unittest.mock import patch
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from .date_utils import split_whole_period_into_chunks
from data_repository.data_repository import retrieve_financial_statements, retrieve_share_price_daily, retrieve_total_amount_of_shares_on_particular_day

ATTRIBUTE_OF_DECISION_INDEX = 2
NUMBER_OF_REPORTS_TO_FETCH_FROM_API = 6 # Not used at the moment

calculate_change_in_share_price = lambda first_day_price, last_day_price: (last_day_price - first_day_price)/first_day_price

def find_out_value_per_dollar_spent_today(companies, date, number_of_reports_in_calculations):
    for item in sorted(calculate_weights(companies, date, number_of_reports_in_calculations), key=lambda x: x[1], reverse=True): print(item)

def calculate_average_share_price_change(companies_tickers, start_date, end_date):
    sum_of_changes = 0.0
    for company in companies_tickers:
        first_day_price = retrieve_share_price_daily(company, start_date)
        last_day_price = retrieve_share_price_daily(company, end_date)
        sum_of_changes += calculate_change_in_share_price(first_day_price, last_day_price)
    return sum_of_changes / len(companies_tickers)

def calculate_investment_value_change(companies_tickers_with_weights, start_date, end_date):
    change_in_invested_money = 0.0
    sum_of_all_bets = sum(abs(weight) for _, weight in companies_tickers_with_weights)
    for ticker, company_bet_weight in companies_tickers_with_weights:
        first_day_price = retrieve_share_price_daily(ticker, start_date)
        last_day_price = retrieve_share_price_daily(ticker, end_date)
        change_in_invested_money += calculate_change_in_share_price(first_day_price, last_day_price) * company_bet_weight / sum_of_all_bets
    return change_in_invested_money

def calculate_weights(companies, date, number_of_reports_for_calculation):
    calculated_weights = []
    for ticker in companies:
        all_shares_amount  = retrieve_total_amount_of_shares_on_particular_day(ticker, date)
        share_price_for_this_date = retrieve_share_price_daily(ticker, date)
        average_real_value_over_analysed_reports = calculate_value_by_free_cash_flow(number_of_reports_for_calculation, ticker, date)
        value_per_dollar_spent = average_real_value_over_analysed_reports / all_shares_amount / share_price_for_this_date
        calculated_weights.append((ticker, value_per_dollar_spent))
    return calculated_weights

def calculate_value_by_free_cash_flow(number_of_reports_for_calculation, ticker, date):
    cash_flow_statements = retrieve_financial_statements("cash_flow_statement", number_of_reports_for_calculation, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, ticker, date)
    return sum(report[ATTRIBUTE_OF_DECISION_INDEX] for report in cash_flow_statements) / len(cash_flow_statements)

# def calculate_weights_modified(index, sub_period_weights, start_date, end_date, period_length_in_days, number_of_reports_for_calculation):
#     if index != 0:
#         modified_weights = []
#         for ticker, weight in sub_period_weights:
#             average_value_this_company_is_traded_per_one_dollar = _calculate_average_market_value_per_dollar([ticker], start_date, end_date, period_length_in_days, number_of_reports_for_calculation)
#             modified_weight = weight/average_value_this_company_is_traded_per_one_dollar # Is it correct?
#             modified_weights.append((ticker, modified_weight))
#         return modified_weights
#     else: return sub_period_weights

# def _calculate_average_market_value_per_dollar(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation):
#     sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days)
#     average_value_per_dollar_spent_across_sub_periods = 0.0
#     for sub_period_start_date, sub_period_end_date in sub_period_dates:
#         sub_period_weights = calculate_weights(companies, sub_period_start_date, number_of_reports_for_calculation)
#         average_value = sum(value for ticker, value in sub_period_weights) / len(sub_period_weights)
#         average_value_per_dollar_spent_across_sub_periods += average_value
#     return average_value_per_dollar_spent_across_sub_periods/len(sub_period_dates)

# UNIT TESTING

# class TestCalculateChangeInSharePrice(unittest.TestCase):

#     def test_increase_in_price(self):
#         self.assertEqual(calculate_change_in_share_price(100, 110), 0.1)

#     def test_decrease_in_price(self):
#         self.assertEqual(calculate_change_in_share_price(100, 90), -0.1)

#     def test_no_change_in_price(self):
#         self.assertEqual(calculate_change_in_share_price(100, 100), 0)

#     def test_zero_initial_price(self):
#         with self.assertRaises(ZeroDivisionError):
#             calculate_change_in_share_price(0, 100)

# class TestCalculateAverageSharePriceChange(unittest.TestCase):

#     @patch('simulation_logic.calculation_utils.retrieve_share_prices_per_period')
#     def test_average_price_increase(self, mock_fetch_prices):
#         # Mock data: Prices increase for both companies
#         mock_fetch_prices.side_effect = [
#             [(100, 110)],  # First company: 10% increase
#             [(200, 240)]   # Second company: 20% increase
#         ]
#         companies = ['COMPANY_A', 'COMPANY_B']
#         average_change = calculate_average_share_price_change(companies, '2021-01-01', '2021-01-31')
#         self.assertAlmostEqual(average_change, 0.15, places=2) # Expecting 15% average increase

#     @patch('simulation_logic.calculation_utils.retrieve_share_prices_per_period')
#     def test_average_price_no_change(self, mock_fetch_prices):
#         # Mock data: No price change for both companies
#         mock_fetch_prices.side_effect = [
#             [(100,), (100,)],  # First company: No change
#             [(200,), (200,)]   # Second company: No change
#         ]
#         companies = ['COMPANY_A', 'COMPANY_B']
#         average_change = calculate_average_share_price_change(companies, '2021-01-01', '2021-01-31')
#         self.assertEqual(average_change, 0)  # Expecting 0% change
