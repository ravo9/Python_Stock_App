from .calculation_utils import calculate_investment_value_change, calculate_average_share_price_change_for_given_companies_in_given_period, calculate_weights
from .date_utils import split_whole_period_into_chunks
from presentation.presentation import present_simulation_results, display_progress
import time

def run_series_of_simulations(companies, start_date, end_date, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY):
    for sub_period_length in SUB_PERIOD_LENGTH_IN_DAYS_ARRAY:
        for number_of_reports_for_calculation in NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY:
            run_simulation(companies, start_date, end_date, sub_period_length, number_of_reports_for_calculation)

def run_simulation(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation):
    
    # Get back in time. Invest given money (e.g. $100) in given companies equally ($100 each).
    change_in_value_of_money_invested_equally = calculate_average_share_price_change_for_given_companies_in_given_period(companies, start_date, end_date)
    
    # Get back in time. Invest given money given companies not equally, but accordingly to the tested strategy (expressed by bets/ weights values).
    change_in_value_of_money_invested_by_using_tested_strategy = _perform_simulation_logic(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation)
    
    present_simulation_results(change_in_value_of_money_invested_equally, change_in_value_of_money_invested_by_using_tested_strategy, period_length_in_days, number_of_reports_for_calculation)
    return change_in_value_of_money_invested_by_using_tested_strategy # Used by otimisation.

def _perform_simulation_logic(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation, original_money = 1000):
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days)
    money = original_money

    for index, (sub_period_start_date, sub_period_end_date) in enumerate(sub_period_dates):
        display_progress(index + 1, len(sub_period_dates), money)
        sub_period_weights = calculate_weights(companies, sub_period_start_date, number_of_reports_for_calculation)

        investment_change = calculate_investment_value_change(sub_period_weights, sub_period_start_date, sub_period_end_date)
        money *= (1 + investment_change)

    return (money - original_money)/ original_money
