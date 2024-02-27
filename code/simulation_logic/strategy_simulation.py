from .calculation_utils import modify_weights, calculate_investment_value_change, calculate_average_share_price_change_for_given_companies_in_given_period, calculate_weights
from .date_utils import split_whole_period_into_chunks
import time

def run_multiple_simulations(companies, start_date, end_date, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY):
    for sub_period_length in SUB_PERIOD_LENGTH_IN_DAYS_ARRAY:
        for number_of_reports_for_calculation in NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY:
            run_simulation(companies, start_date, end_date, sub_period_length, number_of_reports_for_calculation)

def run_simulation(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation):
    # Get back in time. Invest given money (e.g. $100) in given companies equally ($100 each) - tested manually on paper.
    change_in_value_of_money_invested_equally = calculate_average_share_price_change_for_given_companies_in_given_period(companies, start_date, end_date)
    # Get back in time. Invest given money given companies not equally, but accordingly to the tested strategy (expressed by bets/ weights values).
    change_in_value_of_money_invested_by_using_tested_strategy = _perform_simulation_logic(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation)
    _present_simulation_results(change_in_value_of_money_invested_equally, change_in_value_of_money_invested_by_using_tested_strategy, period_length_in_days, number_of_reports_for_calculation)
    return change_in_value_of_money_invested_by_using_tested_strategy # Used by otimisation.

def _perform_simulation_logic(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation, original_money = 1000):
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days)
    money = original_money
    
    # Google Sheets Analysis
    average_value_for_all_companies_across_whole_period = 0.0
    table_data = [['Company'] + [company for company in companies] + ['Sub-Period Average']]
    
    for index, (sub_period_start_date, sub_period_end_date) in enumerate(sub_period_dates):
        _display_progress(index + 1, len(sub_period_dates), money)
        sub_period_weights = calculate_weights(companies, sub_period_start_date, number_of_reports_for_calculation)
        # sub_period_weights = modify_weights(index, sub_period_weights, start_date, sub_period_end_date, period_length_in_days, number_of_reports_for_calculation)
        
        # Google Sheets Analysis
        average_value_for_all_companies_this_sub_period = sum(value for ticker, value in sub_period_weights) / len(sub_period_weights)
        table_data.append([sub_period_start_date] + [value for _, value in sub_period_weights] + [average_value_for_all_companies_this_sub_period])
        average_value_for_all_companies_across_whole_period += average_value_for_all_companies_this_sub_period

        investment_change = calculate_investment_value_change(sub_period_weights, sub_period_start_date, sub_period_end_date)
        money *= (1 + investment_change)
    
    # Google Sheets Analysis
    average_value_for_all_companies_across_whole_period = average_value_for_all_companies_across_whole_period/len(sub_period_dates)
    table_data.append(['Whole-Period Average'] + [average_value_for_all_companies_across_whole_period])
    _save_to_csv(table_data)

    return (money - original_money)/ original_money

import csv
def _save_to_csv(data, file_path="../exported.csv"):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    print(f"Data has been successfully saved to '{file_path}'.")

def _display_progress(acc, total_length, money): print(f"{((acc/total_length) * 100):.2f}%" + " " + str(money), end='\r')

def _present_simulation_results(money_invested_equally, money_invested_according_to_strategy, period_length_in_days, number_of_reports_for_calculation):
    print("SIMULATION: PERIOD: " + str(period_length_in_days) + " DAYS; REPORTS NUMBER: " + str(number_of_reports_for_calculation))
    print("MONEY INVESTED IN GIVEN COMPANIES EQUALLY (AVERAGE): " + "{0:.2%}".format(money_invested_equally))
    print("MONEY INVESTED IN GIVEN COMPANIES USING TESTED STRATEGY: " + "{0:.2%}".format(money_invested_according_to_strategy))

start_time = None
def _measureTime(command):
    global start_time
    if (command == "START"): start_time = time.time()
    if (command == "STOP"):
        execution_time = time.time() - start_time
        print("Execution time:", execution_time, "seconds")
