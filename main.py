from strategy_simulation import fetch_necessary_data_for_experiment, run_multiple_simulations
from config import COMPANIES_SET, START_DATE, END_DATE, ATTRIBUTE_OF_DECISION_INDEX, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY
from constants import DATE_FORMAT

# Main App
fetch_necessary_data_for_experiment(COMPANIES_SET)
run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, ATTRIBUTE_OF_DECISION_INDEX, None, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, "TESTING SET", False)
