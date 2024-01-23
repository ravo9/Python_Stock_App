import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from data_repository import retrieve_share_price_daily, retrieve_total_amount_of_shares_on_particular_day, retrieve_financial_reports
from config import NUMBER_OF_REPORTS_TO_FETCH_FROM_API

def get_weights_for_bets_for_given_companies_for_given_date(companies, date, number_of_reports_for_calculation, ATTRIBUTE_OF_DECISION_INDEX = 2):
    calculated_weights = []
    sum_of_weights = 0.0
    for ticker in companies:
        financial_reports = retrieve_financial_reports(number_of_reports_for_calculation, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, ticker, date)
        all_shares_amount  = retrieve_total_amount_of_shares_on_particular_day(ticker, date)
        share_price_for_this_date = retrieve_share_price_daily(ticker, date)
        average_real_value_over_analysed_reports = sum(report[ATTRIBUTE_OF_DECISION_INDEX] for report in financial_reports) / len(financial_reports)
        value_per_dollar_spent = average_real_value_over_analysed_reports / all_shares_amount / share_price_for_this_date
        calculated_weights.append((ticker, value_per_dollar_spent))
    return calculated_weights
