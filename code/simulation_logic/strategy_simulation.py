import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from simulation_logic.calculation_utils import calculate_investment_value_change, calculate_average_share_price_change_for_given_companies_in_given_period
from date_utils import split_whole_period_into_chunks
from api_utils import fetch_financial_data
from database_utils import save_financial_data, read_all_data_from_database
from simulation_logic.weights_factory import get_weights_for_bets_for_given_companies_for_given_date

def run_multiple_simulations(companies, start_date, end_date, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY):
    for sub_period_length in SUB_PERIOD_LENGTH_IN_DAYS_ARRAY:
        _run_simulation(companies, start_date, end_date, sub_period_length)

def _run_simulation(companies, start_date, end_date, period_length_in_days):
    fetch_necessary_data_for_experiment(companies)
    # Get back in time. Invest given money (e.g. $100) in given companies equally ($100 each) - tested manually on paper.
    change_in_value_of_money_invested_equally = calculate_average_share_price_change_for_given_companies_in_given_period(companies, start_date, end_date)
    # Get back in time. Invest given money given companies not equally, but accordingly to the tested strategy (expressed by bets/ weights values).
    change_in_value_of_money_invested_by_using_tested_strategy = _perform_simulation_logic(companies, start_date, end_date, period_length_in_days)
    _present_simulation_results(change_in_value_of_money_invested_equally, change_in_value_of_money_invested_by_using_tested_strategy)

def _perform_simulation_logic(companies, start_date, end_date, period_length_in_days):
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days)
    original_money = 1000
    money = original_money
    # Todo: it would be good to have also average over time (average of these averages)
    # average_value_per_dollar_spent_across_sub_periods = 0.0
    acc = 1
    for sub_period_start_date, sub_period_end_date in sub_period_dates:
        progress = acc / len(sub_period_dates) * 100
        print(f"{progress:.2f}%", end='\r')
        acc += 1
        sub_period_weights = get_weights_for_bets_for_given_companies_for_given_date(companies, sub_period_start_date)
        # average_value = average_real_value_per_dollar(sub_period_weights, sub_period_start_date)
        # print_average_value_per_dollar_for_companies_for_given_day(sub_period_weights, sub_period_start_date, average_value)
        # average_value_per_dollar_spent_across_sub_periods += average_value
        investment_change = calculate_investment_value_change(sub_period_weights, (sub_period_end_date == end_date), sub_period_start_date, sub_period_end_date)
        money *= (1 + investment_change)
    # print("AVERAGE VALUE PER DOLLAR SPENT ACROSS WHOLE PERIOD: " + str(average_value_per_dollar_spent_across_sub_periods/len(sub_period_dates)))
    return (money - original_money)/ original_money

def fetch_necessary_data_for_experiment(companies):
    save_financial_data(fetch_financial_data(companies))
    # read_all_data_from_database()

def print_average_value_per_dollar_for_companies_for_given_day(calculated_weights, date, average_value):
    if calculated_weights: print(f"Average value per dollar spent for given companies on {date} : {average_value}")

def average_real_value_per_dollar(real_values, date):
    if not real_values: return None
    return sum(value for _, value in real_values) / len(real_values)

def _present_simulation_results(money_invested_equally, money_invested_according_to_strategy):
    print("MONEY INVESTED IN GIVEN COMPANIES EQUALLY (AVERAGE): " + "{0:.2%}".format(money_invested_equally))
    print("MONEY INVESTED IN GIVEN COMPANIES USING TESTED STRATEGY: " + "{0:.2%}".format(money_invested_according_to_strategy))
