FINANCIAL_MODELING_COMPANIES_SET = [
    'MSFT', 'NFLX', 'AAPL', # Tested
    'META', 'NVDA', 'VZ', 'KO', # Tested
    'MCD', 'JNJ', 'SBUX', # Tested
    # AMZN, GOOGL, TSLA - split in 2022
    # META, NVDA - split 2021
    # AAPL - split 2020
    'AMZN', 'GOOGL', 'TSLA'
    # Maybe it's good idea to provide more various companies (smaller).
]
# * By Tested it has enough reports on the server, and didn't have split in tested period.
# Problem: splits (they're not taken into account by share price and amount of shares in the same way).
# Problem: single company is not giving the same result as average investment - in some cases (e.g. 90 days period)
COMPANIES_SET = FINANCIAL_MODELING_COMPANIES_SET

START_DATE = '2023-01-01'
END_DATE = '2024-01-01'

# Problem: Why quite often longer period performs better than short one?
SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [100, 200]
NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [8]
