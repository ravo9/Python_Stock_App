from simulation_logic.strategy_simulation import run_multiple_simulations, calculate_average_market_value_per_dollar
from config import COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY
import unittest
from simulation_logic.calculation_utils import TestCalculateChangeInSharePrice, TestCalculateAverageSharePriceChange
from simulation_logic.weights_factory import get_weights_for_bets
from database_utils import read_all_data_from_database
import cProfile
import pstats

def run_unit_tests():
    unittest.main()

def find_out_value_per_dollar_spent_today(companies, date, number_of_reports_in_calculations):
    for item in sorted(get_weights_for_bets(companies, date, number_of_reports_in_calculations), key=lambda x: x[1], reverse=True):
        print(item)

def run_profiler():
    cProfile.run('run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY)', 'profile_stats')
    p = pstats.Stats('profile_stats')
    p.sort_stats('time').print_stats(10) # Print the top 10 time-consuming functions

# FUNCTIONALITY (uncomment to run):
find_out_value_per_dollar_spent_today(COMPANIES_SET, END_DATE, 8)
# run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY)
# run_unit_tests()
# read_all_data_from_database()
# run_profiler()
# calculate_average_market_value_per_dollar(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY[0], NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY[0])
