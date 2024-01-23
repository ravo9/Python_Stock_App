FINANCIAL_MODELING_COMPANIES_SET = [
    'TSLA', 'MSFT', 'NFLX', 'AMZN', 'GOOGL', # Tested with at least x reports
    'AAPL', 'SQ', 'NVDA', 'KO', 'VZ', # Tested with at least x reports
]
POLYGON_AVAILABLE_COMPANIES_SET = [
    'TSLA', 'MSFT', 'NFLX', 'AMZN', 'GOOGL', # Tested with at least 20 reports
    'AAPL', 'SQ', 'NVDA', 'KO', 'VZ', # Tested with at least 20 reports
    # 'PYPL', 'BLK', # Tested with at least 20 reports
     # 'BRK.B', 'MRNA', 'BYND' # Issues
]
# NOT ENOUGH QUARTER REPORTS ON POLYGON: META (5), DIS (18 with net_cash_flow), PTON (17 with n_c_f), ALPP (6 with n_c_f), PLTR (12 with n_c_f)
# NOT AVAILABLE ON POLYGON: SPOT, BABA, OCDO/OCDO.L, HMC, BAYN, BARC, NIO, ABEPF, XPEV


START_DATE = '2023-01-01'

END_DATE = '2024-01-09'

COMPANIES_SET = ['META']

SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [90]

NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY = [8]

NUMBER_OF_REPORTS_TO_FETCH_FROM_API = 6 # Todo: automate it
