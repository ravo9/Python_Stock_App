from simulation_logic.strategy_simulation import run_multiple_simulations
from config import COMPANIES_SET, START_DATE, END_DATE, ATTRIBUTE_OF_DECISION_INDEX, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY

# Main App
run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, ATTRIBUTE_OF_DECISION_INDEX, None, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY)
