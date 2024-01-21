import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database_utils import get_stored_financial_reports_if_available
from data_repository import retrieve_share_price_daily, retrieve_total_amount_of_shares_on_particular_day
from config import NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION, NUMBER_OF_REPORTS_TO_FETCH_FROM_API

def get_weights_for_bets_for_given_companies_for_given_date(companies, date, ATTRIBUTE_OF_DECISION_INDEX = 2):
    calculated_weights = []
    sum_of_weights = 0.0
    for company_ticker in companies:
        financial_reports = get_stored_financial_reports_if_available(NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION, NUMBER_OF_REPORTS_TO_FETCH_FROM_API, company_ticker, date)
        all_shares_amount  = retrieve_total_amount_of_shares_on_particular_day(company_ticker, date)
        share_price_for_this_date = retrieve_share_price_daily(company_ticker, date)
        average_value_of_decision_attribute_over_fetched_reports = sum(report[ATTRIBUTE_OF_DECISION_INDEX] for report in financial_reports) / len(financial_reports)
        value_per_dollar_spent = average_value_of_decision_attribute_over_fetched_reports / all_shares_amount / share_price_for_this_date
        calculated_weights.append((company_ticker, value_per_dollar_spent))
    return calculated_weights
