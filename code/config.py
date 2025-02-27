COMPANIES_SET = ['MSFT', 'NFLX', 'TSLA', 'NVDA', 'AAPL', 'SBUX']
START_DATE = '2023-01-01'
END_DATE = '2024-01-01'
SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [150]
NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [6]

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

# Todo/problem: splits (they're not taken into account by share price and amount of shares in the same way).
# By 'tested' it means that it has enough reports on the server, and didn't have split in tested period (01.01.22 - 01.01.24).

# Problem: Why often longer period performs better than short one?

# Todo/problem: BABA - Chinese currency