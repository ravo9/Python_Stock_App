import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from date_utils import increase_date_by_day
from database_utils import read_db_share_price_in_particular_day, get_most_recent_financial_reports_for_given_company_until_particular_date
from constants import DATE_FORMAT

INVESTMENT_VALUE_NUMBER_OF_PERIODS = 4

# New approach  "overpriced_will_drop_and_underpriced_will_raise"
def get_weights_for_bets_for_given_companies_for_given_date(companies, attribute_of_decision_index, given_date):
    calculated_weights = []
    normalized_weights = []
    sum_of_weights = 0.0
    for company_ticker in companies:
        weight = _get_investment_value_for_given_company_for_given_date_n_periods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date)
        if (weight > 0):
            calculated_weights.append((company_ticker, weight))
            sum_of_weights = sum_of_weights + weight
        # else if (weight < 0):
        #     calculated_weights.append((company_ticker, weight))
        #     sum_of_weights = sum_of_weights + (weight * -1)
    average_weight = sum_of_weights / len(calculated_weights)
    recalculated_weights = []
    sum_of_recalculated_weights = 0.0
    for weight in calculated_weights:
        company_ticker = weight[0]
        weight_value = weight[1]
        # Only positive numbers
        recalculated_weight = weight_value - average_weight
        recalculated_weights.append((company_ticker, recalculated_weight))
        if recalculated_weight > 0:
            sum_of_recalculated_weights += recalculated_weight
        if recalculated_weight < 0:
            sum_of_recalculated_weights += (recalculated_weight * -1)
    for weight in recalculated_weights:
        company_ticker = weight[0]
        weight_value = weight[1]
        normalized_weight = weight_value / sum_of_recalculated_weights
        normalized_weights.append((company_ticker, normalized_weight))
    return normalized_weights

def _get_investment_value_for_given_company_for_given_date_n_periods(number_of_periods, company_ticker, attribute_of_decision_index, date):
    financial_reports = get_most_recent_financial_reports_for_given_company_until_particular_date(number_of_periods, company_ticker, date)
    if financial_reports == []:
        raise ValueError("ERROR: Empty list")
    average_attribute_of_decision_value = 0.0
    for report in financial_reports:
        index_of_amount_of_shares = 4
        decision_value = report[attribute_of_decision_index] / report[index_of_amount_of_shares]
        average_attribute_of_decision_value = average_attribute_of_decision_value + decision_value
    average_attribute_of_decision_value = average_attribute_of_decision_value / len(financial_reports)
    # attributeOfdecision_value = financial_reports[0][attribute_of_decision_index]
    share_price_for_this_date = None
    date_variable = date
    for i in range(0, 5): # I want to try to increase 4 times, on 5th attempt - print error. The loop works in 0 - (n-1) range.
        share_price_for_this_date = read_db_share_price_in_particular_day(company_ticker, date_variable)
        if (share_price_for_this_date == None):
            date_variable = increase_date_by_day(date_variable, DATE_FORMAT)
        else:
            break
    investment_value = average_attribute_of_decision_value / share_price_for_this_date
    return investment_value

# Unused code (to be researched)

# def _calculate_average_investment_value_in_this_date_for_given_companies(companies, attribute_of_decision_index, given_date):
#     sum_of_investment_values = 0.0
#     result = "" + given_date
#     for company_ticker in companies:
#         investment_value = get_investment_value_for_given_company_for_given_date_n_periods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date)
#         sum_of_investment_values = sum_of_investment_values + investment_value
#         result = result + " " + str(investment_value)
#     average_investment_value = sum_of_investment_values / len(companies)
#     result = result + " " + str(average_investment_value)
#     print(result)

# # Old approach - only the difference part left over here
# def get_weights_for_bets_for_given_companies_for_given_date_buy_all_just_less_of_overpriced_and_more_of_underpriced(companies, attribute_of_decision_index, given_date):
#     for weight in calculated_weights:
#         company_ticker = weight[0]
#         weight_value = weight[1]
#         if weight_value > 0:
#             normalized_weight = weight_value / sum_of_weights
#             normalized_weights.append((company_ticker, normalized_weight))
#         # else if (weight_value < 0):
