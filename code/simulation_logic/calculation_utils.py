import sys
import os
import unittest
from unittest.mock import patch
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from data_repository.data_repository import retrieve_financial_statements, retrieve_share_price_daily, retrieve_share_prices_per_period, retrieve_total_amount_of_shares_on_particular_day

ATTRIBUTE_OF_DECISION_INDEX = 2

calculate_change_in_share_price = lambda first_day_price, last_day_price: (last_day_price - first_day_price)/first_day_price

# Not used at the moment
NUMBER_OF_REPORTS_TO_FETCH_FROM_API = 6

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
        change_in_invested_money += calculate_change_in_share_price(first_day_price, last_day_price) * company_bet_weight / sum_of_all_bets
    return change_in_invested_money

def calculate_weights(companies, date, number_of_reports_for_calculation):
    calculated_weights = []
    for ticker in companies:
        all_shares_amount  = retrieve_total_amount_of_shares_on_particular_day(ticker, date)
        share_price_for_this_date = retrieve_share_price_daily(ticker, date)
        average_real_value_over_analysed_reports = calculate_value_by_free_cash_flow(number_of_reports_for_calculation, ticker, date)
        # average_real_value_over_analysed_reports = calculate_value_by_intrinsic_value(ticker, date, number_of_reports_for_calculation, 5)
        value_per_dollar_spent = average_real_value_over_analysed_reports / all_shares_amount / share_price_for_this_date
        calculated_weights.append((ticker, value_per_dollar_spent))
    return calculated_weights

def find_out_value_per_dollar_spent_today(companies, date, number_of_reports_in_calculations):
    for item in sorted(calculate_weights(companies, date, number_of_reports_in_calculations), key=lambda x: x[1], reverse=True): print(item)

def calculate_value_by_free_cash_flow(number_of_reports_for_calculation, ticker, date):
    cash_flow_statements = retrieve_financial_statements("cash_flow_statement", number_of_reports_for_calculation, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, ticker, date)
    return sum(report[ATTRIBUTE_OF_DECISION_INDEX] for report in cash_flow_statements) / len(cash_flow_statements)

def calculate_value_by_intrinsic_value(ticker, date, num_periods, projection_years):
    cash_flow_statements = retrieve_financial_statements("cash_flow_statement", num_periods, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, ticker, date)
    income_statements = retrieve_financial_statements("income_statement", num_periods, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, ticker, date)
    balance_sheets = retrieve_financial_statements("balance_sheet", num_periods, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, ticker, date)
    average_fcf = calculate_average_free_cash_flow(cash_flow_statements, num_periods)
    growth_rate = calculate_growth_rate(cash_flow_statements)
    discount_rate = calculate_discount_rate(income_statements, balance_sheets, num_periods)
    present_value_fcf = 0
    for year in range(1, projection_years + 1):
        future_fcf = average_fcf * (1 + growth_rate) ** year
        discounted_fcf = future_fcf / (1 + discount_rate) ** year
        present_value_fcf += discounted_fcf
    return float(present_value_fcf)

def calculate_average_free_cash_flow(cash_flow_statements, num_years):
    free_cash_flows_only = [row[ATTRIBUTE_OF_DECISION_INDEX] for row in cash_flow_statements]
    if len(free_cash_flows_only) < num_years: return "Insufficient data"
    return sum(free_cash_flows_only[-num_years:]) / num_years

def calculate_growth_rate(cash_flow_statements):
    fcf_values = [row[ATTRIBUTE_OF_DECISION_INDEX] for row in cash_flow_statements]
    if not fcf_values or len(fcf_values) == 0: print("No FCF data provided")
    return sum(fcf_values) / len(fcf_values)

def calculate_discount_rate(income_statements, balance_sheets, num_years):
    # "Cost of debt" is interest_expense / total_debt - our simplified discount rate.
    if not income_statements or len(income_statements) == 0: print("No Income Statements provided")
    if not balance_sheets or len(balance_sheets) == 0: print("No Balance Sheets provided")
    interest_expense_only = [row[ATTRIBUTE_OF_DECISION_INDEX] for row in income_statements]
    if len(interest_expense_only) < num_years: return "Insufficient data"
    average_interest_expense = sum(interest_expense_only[-num_years:]) / num_years
    total_debt_only = [row[ATTRIBUTE_OF_DECISION_INDEX] for row in balance_sheets]
    if len(total_debt_only) < num_years: return "Insufficient data"
    average_total_debt = sum(total_debt_only[-num_years:]) / num_years
    if average_total_debt == 0: return "Total debt cannot be zero"
    return average_interest_expense / average_total_debt

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
