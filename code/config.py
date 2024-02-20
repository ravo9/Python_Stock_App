# Test Scenario 1
# average: 15.06%
# my best result: 16.75%
# best setting: 20 days; 10 reports; strategy freeCashFlow
# COMPANIES_SET = ['MSFT', 'NFLX', 'VZ', 'KO', 'MCD', 'JNJ', 'SBUX', 'DIS', 'ORCL', 'O', 'JPM']
# START_DATE = '2023-01-01'
# END_DATE = '2024-01-01'
# SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [30, 20]
# NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [6, 10]

# Test Scenario 2
# average: -7.89%
# my best result: 14.36%
# best setting: 30 days; 6 reports; strategy freeCashFlow
# COMPANIES_SET = ['MSFT', 'NFLX', 'VZ', 'KO', 'MCD', 'JNJ', 'SBUX', 'DIS', 'ORCL', 'O', 'JPM']
# START_DATE = '2022-01-01'
# END_DATE = '2024-01-01'
# SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [30, 20]
# NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [6, 10]

# Test Scenario 3
# average: 9.83%
# my best result: 31.26%
# best setting: 30 days; 6 reports; strategy freeCashFlow
# COMPANIES_SET = ['MSFT', 'NFLX', 'VZ', 'KO', 'MCD', 'JNJ', 'SBUX', 'DIS', 'ORCL', 'O', 'JPM']
# START_DATE = '2021-01-01'
# END_DATE = '2024-01-01'
# SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [30, 20]
# NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [6, 10]

# Test Scenario 4
# average: 4.64%
# my best result: 27.37%
# best setting: 30 days; 6 reports; strategy freeCashFlow
# COMPANIES_SET = ['MSFT', 'NFLX', 'VZ', 'KO', 'MCD', 'JNJ', 'SBUX', 'DIS', 'ORCL', 'O', 'JPM','WMT', 'XOM', 'UNH', 'CVS', 'MCK', 'CVX']
# START_DATE = '2022-01-01'
# END_DATE = '2024-01-01'
# SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [30, 20]
# NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [6, 10]

# FINANCIAL_MODELING_COMPANIES_SET = [
#     'MSFT', 'NFLX', # Tested
#     'VZ', 'KO', 'MCD', 'JNJ', 'SBUX', # Tested
#     'BABA', 'DIS', 'ORCL', 'O', 'JPM', # Tested
#
#     # 'ALPP', # split in 2023
#     # 'AMZN', 'GOOGL', 'TSLA', # split in 2022
#     # 'META', 'NVDA', # split 2021
#     # 'AAPL', # split 2020
#     # 'UNH', 'CVS' # last split 2005
#     # 'CVX', # last split 2004
#     # 'XOM', # last split 2001
#     # 'WMT', # last split 1999
#     # 'MCK', # last split 1998
# ]

COMPANIES_SET = ['XOM', 'UNH', 'CVS', 'MCK', 'CVX']
START_DATE = '2022-01-01'
END_DATE = '2024-01-01'
SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [130]
NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [6]

# * By Tested it means that it has enough reports on the server, and didn't have split in tested period (01.01.22 - 01.01.24).
# Problem: splits (they're not taken into account by share price and amount of shares in the same way).
# Problem: Why often longer period performs better than short one?
# Problem: ABA - Chinese currency!
