import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database_utils import fetch_related_financial_reports, fetch_price_in_particular_day_dynamically
from api_utils import fetch_total_amount_of_shares_on_particular_day
from config import INVESTMENT_VALUE_NUMBER_OF_PERIODS

# Todo: maybe it would be useful to find out the average "value per dollar" at a given time on the market
def get_weights_for_bets_for_given_companies_for_given_date(companies, attribute_of_decision_index, date):
    calculated_weights = []
    sum_of_weights = 0.0
    for company_ticker in companies:
        financial_reports = fetch_related_financial_reports(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, date)
        all_shares_amount  = fetch_total_amount_of_shares_on_particular_day(company_ticker, date)
        share_price_for_this_date = fetch_price_in_particular_day_dynamically(company_ticker, date)
        average_value_of_decision_attribute_over_fetched_reports = sum(report[attribute_of_decision_index] for report in financial_reports) / len(financial_reports)
        value_per_dollar_spent = average_value_of_decision_attribute_over_fetched_reports / all_shares_amount / share_price_for_this_date
        calculated_weights.append((company_ticker, value_per_dollar_spent))
    return calculated_weights
