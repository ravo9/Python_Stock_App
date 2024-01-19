import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database_utils import retrieve_related_financial_reports
from api_utils import fetch_total_amount_of_shares_on_particular_day, fetch_price_in_particular_day_dynamically
from config import NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION

ATTRIBUTE_OF_DECISION_INDEX = 3

def get_weights_for_bets_for_given_companies_for_given_date(companies, date):
    calculated_weights = []
    sum_of_weights = 0.0
    for company_ticker in companies:
        financial_reports = retrieve_related_financial_reports(NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION, company_ticker, date)
        all_shares_amount  = fetch_total_amount_of_shares_on_particular_day(company_ticker, date)
        share_price_for_this_date = fetch_price_in_particular_day_dynamically(company_ticker, date)
        average_value_of_decision_attribute_over_fetched_reports = sum(report[ATTRIBUTE_OF_DECISION_INDEX] for report in financial_reports) / len(financial_reports)
        value_per_dollar_spent = average_value_of_decision_attribute_over_fetched_reports / all_shares_amount / share_price_for_this_date
        calculated_weights.append((company_ticker, value_per_dollar_spent))
    return calculated_weights
