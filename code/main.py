from simulation_logic.strategy_simulation import run_multiple_simulations, fetch_necessary_data_for_experiment
from config import COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY
import unittest
from simulation_logic.calculation_utils import TestCalculateChangeInSharePrice, TestCalculateAverageSharePriceChange
from simulation_logic.weights_factory import get_weights_for_bets_for_given_companies_for_given_date
from database_utils import read_all_data_from_database
import time

def run_unit_tests():
    unittest.main()

def find_out_value_per_dollar_spent_today_for_given_companies():
    fetch_necessary_data_for_experiment(COMPANIES_SET)
    weights_today = get_weights_for_bets_for_given_companies_for_given_date(COMPANIES_SET, END_DATE)
    weights_today = sorted(weights_today, key=lambda x: x[1], reverse=True)
    for item in weights_today: print(item)

# Main App
# run_unit_tests()
# find_out_value_per_dollar_spent_today_for_given_companies()
start_time = time.time()
run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY)
total_time = time.time() - start_time
print(f"Total execution time: {total_time:.2f} seconds")
