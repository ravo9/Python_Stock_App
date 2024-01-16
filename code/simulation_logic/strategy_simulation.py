import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from simulation_logic.calculation_utils import calculate_investment_value_change, calculate_average_share_price_change_for_given_companies_in_given_period
from printing_utils import print_simulation_results
from date_utils import split_whole_period_into_chunks
from database_utils import fetch_necessary_data_for_experiment
from simulation_logic.weights_factory import get_weights_for_bets_for_given_companies_for_given_date
from constants import DATE_FORMAT

def run_multiple_simulations(companies, start_date, end_date, attribute_of_decision_index, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY):
    for sub_period_length_in_days in SUB_PERIOD_LENGTH_IN_DAYS_ARRAY:
        _run_simulation(companies, start_date, end_date, attribute_of_decision_index, sub_period_length_in_days)

def _run_simulation(companies, start_date, end_date, attribute_of_decision_index, period_length_in_days):
    # Prepare environment for the testing.
    fetch_necessary_data_for_experiment(companies)
    # Get back in time. Invest given money (e.g. $100) in given companies equally ($100 each) - tested manually on paper.
    # change_in_value_of_money_invested_equally = calculate_average_share_price_change_for_given_companies_in_given_period(companies, start_date, end_date)
    # # Get back in time. Invest given money given companies not equally, but accordingly to the tested strategy (expressed by bets/ weights values).
    # change_in_value_of_money_invested_according_to_tested_strategy = _perform_simulation_logic(companies, start_date, end_date, period_length_in_days,attribute_of_decision_index)
    # # Compare both results.
    # _present_simulation_results(change_in_value_of_money_invested_equally, change_in_value_of_money_invested_according_to_tested_strategy)

def _perform_simulation_logic(companies, start_date, end_date, period_length_in_days, attribute_of_decision_index):
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days, DATE_FORMAT)
    original_money = 1000
    money = original_money
    for sub_period_start_date, sub_period_end_date in sub_period_dates:
        sub_period_weights = get_weights_for_bets_for_given_companies_for_given_date(companies, attribute_of_decision_index, sub_period_start_date)
        investment_change = calculate_investment_value_change(sub_period_weights, (sub_period_end_date == end_date), sub_period_start_date, sub_period_end_date)
        money *= (1 + investment_change)
    return (money - original_money)/ original_money

def _present_simulation_results(money_invested_equally, money_invested_according_to_strategy):
    print_simulation_results(money_invested_equally, money_invested_according_to_strategy)
