from simulation_logic.strategy_simulation import run_multiple_simulations, calculate_average_market_value_per_dollar
from simulation_logic.calculation_utils import find_out_value_per_dollar_spent_today, TestCalculateChangeInSharePrice, TestCalculateAverageSharePriceChange # For unit tests the tests has to be imported to 'main'.
from data_repository.database_utils import read_all_data_from_database
from config import COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY
from testing_and_optimisation.optimisation_utils import run_profiler
from testing_and_optimisation.testing_manager import run_unit_tests

# FUNCTIONALITY (uncomment to run):
# find_out_value_per_dollar_spent_today(COMPANIES_SET, END_DATE, 8)
run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY)
# calculate_average_market_value_per_dollar(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY[0], NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY[0])

# DEVELOPMENT TOOLS (uncomment to run):
# run_unit_tests()
# read_all_data_from_database()
# run_profiler('run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY)')
