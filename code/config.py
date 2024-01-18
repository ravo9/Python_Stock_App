# COMPANIES_SET = ['TSLA', 'MSFT', 'NFLX', 'AMZN', 'GOOGL', 'PYPL', 'DIS', 'AAPL', 'SQ']
COMPANIES_SET = ['TSLA', 'MSFT', 'NFLX']
# COMPANIES_SET = []
# NOT AVAILABLE ON POLYGON: SPOT

START_DATE = '2022-01-01'
# START_DATE = '2023-12-01'

END_DATE = '2024-01-08'
# Todo check: making problem with current date as END_DATE for
# fetch_total_amount_of_shares_on_particular_day - delay around 10 days sometimes

SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [20]

ATTRIBUTE_OF_DECISION_INDEX = 3

# Todo: automate with the INVESTMENT_VALUE_NUMBER_OF_PERIODS
# AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH doesn't work precisely. Sometimes fetches
# 1 or 2 reports less than should.
# AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH = 15
AMOUNT_OF_HISTORIC_REPORTS_TO_FETCH = 6
INVESTMENT_VALUE_NUMBER_OF_PERIODS = 4
