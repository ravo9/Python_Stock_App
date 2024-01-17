import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from date_utils import increase_date_by_day
from database_utils import find_share_price_for_this_date, fetch_related_financial_reports
from constants import DATE_FORMAT
from api_utils import fetch_total_amount_of_shares_on_particular_day

INVESTMENT_VALUE_NUMBER_OF_PERIODS = 4

def get_weights_for_bets_for_given_companies_for_given_date(companies, attribute_of_decision_index, given_date):
    calculated_weights = []
    sum_of_weights = 0.0
    for company_ticker in companies:
        weight = _calculate_weight(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date)
        if (weight > 0): # else -> negative numbers problem
            calculated_weights.append((company_ticker, weight))
    return calculated_weights

def _calculate_weight(number_of_periods, company_ticker, attribute_of_decision_index, date):
    financial_reports = fetch_related_financial_reports(number_of_periods, company_ticker, date)
    all_shares_amount  = fetch_total_amount_of_shares_on_particular_day(company_ticker, date)
    share_price_for_this_date = find_share_price_for_this_date(date, company_ticker)
    average_value_of_decision_attribute_over_fetched_reports = sum(report[attribute_of_decision_index] for report in financial_reports) / len(financial_reports)
    value_per_dollar_spent = average_value_of_decision_attribute_over_fetched_reports / all_shares_amount / share_price_for_this_date
    return value_per_dollar_spent

# Todo: extract useful pieces of this unsused code logic into "modification" functions

    # average_weight = sum_of_weights / len(calculated_weights)
    # recalculated_weights = []
    # sum_of_recalculated_weights = 0.0
    # for company_ticker, weight_value in calculated_weights:
    #     recalculated_weight = weight_value - average_weight
    #     recalculated_weights.append((company_ticker, recalculated_weight))
    #     sum_of_recalculated_weights += abs(recalculated_weight) # Only positive numbers
    # for company_ticker, weight_value in recalculated_weights:
    #     normalized_weight = weight_value / sum_of_recalculated_weights
    #     normalized_weights.append((company_ticker, normalized_weight))
    # return normalized_weights

# def _calculate_average_investment_value_in_this_date_for_given_companies(companies, attribute_of_decision_index, given_date):
#     sum_of_investment_values = 0.0
#     result = "" + given_date
#     for company_ticker in companies:
#         investment_value = get_investment_value_for_given_company_for_given_date_n_periods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date)
#         sum_of_investment_values = sum_of_investment_values + investment_value
#         result = result + " " + str(investment_value)
#     average_investment_value = sum_of_investment_values / len(companies)
#     result = result + " " + str(average_investment_value)
