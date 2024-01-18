import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database_utils import fetch_related_financial_reports, fetch_price_in_particular_day_dynamically
from constants import DATE_FORMAT
from api_utils import fetch_total_amount_of_shares_on_particular_day

INVESTMENT_VALUE_NUMBER_OF_PERIODS = 4

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

# def _calculate_average_investment_value_in_this_date_for_given_companies(companies, attribute_of_decision_index, given_date):
#     sum_of_investment_values = 0.0
#     result = "" + given_date
#     for company_ticker in companies:
#         investment_value = get_investment_value_for_given_company_for_given_date_n_periods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date)
#         sum_of_investment_values = sum_of_investment_values + investment_value
#         result = result + " " + str(investment_value)
#     average_investment_value = sum_of_investment_values / len(companies)
#     result = result + " " + str(average_investment_value)
