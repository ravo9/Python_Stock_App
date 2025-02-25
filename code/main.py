from simulation_logic.strategy_simulation import run_series_of_simulations, run_simulation
from config import COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY
from testing_and_optimisation.optimisation_utils import run_profiler, find_optimal_parameters
from testing_and_optimisation.testing_manager import run_unit_tests
# from data_repository.data_repository import TestRetrieveFinancialReports, TestRetrieveSharePriceDaily, TestRetrieveTotalAmountOfSharesOnParticularDay
# from simulation_logic.calculation_utils import find_out_value_per_dollar_spent_today, TestCalculateChangeInSharePrice, TestCalculateAverageSharePriceChange, TestCalculateChangeInSharePrice, TestCalculateAverageSharePriceChange # For unit tests the tests has to be imported to 'main'.


# MAIN FUNCTIONALITY (uncomment to run):
run_series_of_simulations(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY)


###############################################################################################################

# SIDEFUNCTIONALITY (uncomment to run):
# find_out_value_per_dollar_spent_today(COMPANIES_SET, '2024-01-26', NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY[0])

# DEVELOPMENT TOOLS (uncomment to run):
# run_unit_tests()
# run_profiler('run_series_of_simulations(COMPANIES_SET, START_DATE, END_DATE, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY)')
# find_optimal_parameters(run_simulation, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY)