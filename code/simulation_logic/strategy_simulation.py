import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from simulation_logic.calculation_utils import calculate_change_in_investment_value_using_provided_weights, calculate_average_share_price_change_for_given_companies_in_given_period
from printing_utils import print_money_after_all_changes_according_to_my_strategy, print_money_after_all_changes_according_to_my_strategy_as_percentage, print_my_strategy_minus_average_change, print_average_change_of_given_companies_in_given_period
from date_utils import split_whole_period_into_chunks
from database_utils import fetch_necessary_data_for_experiment
from simulation_logic.weights_factory import get_weights_for_bets_for_given_companies_for_given_date
from constants import DATE_FORMAT

def run_multiple_simulations(companies, start_date, end_date, attribute_of_decision_index, whole_period_length, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY):
    for sub_period_length_in_days in SUB_PERIOD_LENGTH_IN_DAYS_ARRAY:
        _run_simulation(companies, start_date, end_date, attribute_of_decision_index, whole_period_length, sub_period_length_in_days)

def _run_simulation(companies, start_date, end_date, attribute_of_decision_index, whole_period_length, period_length_in_days):
    fetch_necessary_data_for_experiment(companies)
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days, DATE_FORMAT)
    money_after_changes_as_percentage = _perform_simulation_logic(sub_period_dates, companies, end_date, attribute_of_decision_index)
    _present_simulation_results(companies, start_date, end_date, money_after_changes_as_percentage)

def _perform_simulation_logic(sub_period_dates, companies, end_date, attribute_of_decision_index):
    original_money = 1000
    money = original_money
    for sub_period_start_date, sub_period_end_date in sub_period_dates:
        is_last_sub_period = (sub_period_end_date == end_date)
        sub_period_weights = get_weights_for_bets_for_given_companies_for_given_date(companies, attribute_of_decision_index, sub_period_start_date)
        investment_change = calculate_change_in_investment_value_using_provided_weights(sub_period_weights, is_last_sub_period, sub_period_start_date, sub_period_end_date)
        money *= (1 + investment_change)
    return (money - original_money)/ original_money

def _present_simulation_results(companies, start_date, end_date, money_after_changes_as_percentage):
    print_money_after_all_changes_according_to_my_strategy_as_percentage(money_after_changes_as_percentage)
    average_change = calculate_average_share_price_change_for_given_companies_in_given_period(companies, start_date, end_date)
    print_average_change_of_given_companies_in_given_period(average_change)
    my_strategy_to_average  = money_after_changes_as_percentage - average_change
    print_my_strategy_minus_average_change(my_strategy_to_average)
