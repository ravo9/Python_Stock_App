from date_utils import increase_date_by_day
from database_utils import read_db_share_price_in_particular_day, get_most_recent_income_statement_for_given_company_for_given_date, get_most_recent_income_statement_for_given_company_for_given_date_n_periods, get_most_recent_income_statement_for_given_company_for_given_date_company_outlook_n_periods
from constants import DATE_FORMAT
from printing_utils import print_average_weight, print_recalculated_normalized_weight, print_investment_value_calculations, print_normalized_weight

INVESTMENT_VALUE_NUMBER_OF_PERIODS = 4


def get_weights_for_bets_for_given_companies_for_given_date(companies, attribute_of_decision_index, given_date, debug_mode):
    calculate_average_investment_value_in_this_date_for_given_companies(companies, attribute_of_decision_index, given_date, debug_mode)
    return get_weights_for_bets_for_given_companies_for_given_date_bet_that_overpriced_will_drop_and_underpriced_will_raise(companies, attribute_of_decision_index, given_date, debug_mode)


def calculate_average_investment_value_in_this_date_for_given_companies(companies, attribute_of_decision_index, given_date, debug_mode):
    sum_of_investment_values = 0.0
    result = "" + given_date
    for company_ticker in companies:
        investment_value = get_investment_value_for_given_company_for_given_date_n_periods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date, debug_mode)
        sum_of_investment_values = sum_of_investment_values + investment_value
        result = result + " " + str(investment_value)
    average_investment_value = sum_of_investment_values / len(companies)
    result = result + " " + str(average_investment_value)
    print(result)


# New approach
def get_weights_for_bets_for_given_companies_for_given_date_bet_that_overpriced_will_drop_and_underpriced_will_raise(companies, attribute_of_decision_index, given_date, debug_mode):
    calculated_weights = []
    normalized_weights = []
    sum_of_weights = 0.0

    for company_ticker in companies:
        weight = get_investment_value_for_given_company_for_given_date_n_periods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date, debug_mode)

        if (weight > 0):
            calculated_weights.append((company_ticker, weight))
            sum_of_weights = sum_of_weights + weight
        # else if (weight < 0):
        #     calculated_weights.append((company_ticker, weight))
        #     sum_of_weights = sum_of_weights + (weight * -1)

    number_of_weights = len(calculated_weights)
    average_weight = sum_of_weights / number_of_weights
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

    print_average_weight(average_weight, debug_mode)

    for weight in recalculated_weights:
        company_ticker = weight[0]
        weight_value = weight[1]

        normalized_weight = weight_value / sum_of_recalculated_weights
        normalized_weights.append((company_ticker, normalized_weight))
        print_recalculated_normalized_weight(company_ticker, normalized_weight, debug_mode)

    return normalized_weights


# Old approach - not sure if still works!
def get_weights_for_bets_for_given_companies_for_given_date_buy_all_just_less_of_overpriced_and_more_of_underpriced(companies, attribute_of_decision_index, given_date, debug_mode):
    calculated_weights = []
    normalized_weights = []
    sum_of_weights = 0.0

    for company_ticker in companies:
        weight = get_investment_value_for_given_company_for_given_date_n_periods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attribute_of_decision_index, given_date, debug_mode)

        if weight > 0:
            calculated_weights.append((company_ticker, weight))
            sum_of_weights = sum_of_weights + weight
        # else if (weight < 0):
        #     calculated_weights.append((company_ticker, weight))
        #     sum_of_weights = sum_of_weights + (weight * -1)

    for weight in calculated_weights:
        company_ticker = weight[0]
        weight_value = weight[1]

        if weight_value > 0:
            normalized_weight = weight_value / sum_of_weights
            normalized_weights.append((company_ticker, normalized_weight))
            print_normalized_weight(company_ticker, normalized_weight, debug_mode)
        # else if (weight_value < 0):

    return normalized_weights


def get_investment_value_for_given_company_for_given_date_n_periods(number_of_periods, company_ticker, attribute_of_decision_index, date, debug_mode = False):
    # most_recent_income_statements_for_this_date = get_most_recent_income_statement_for_given_company_for_given_date_n_periods(number_of_periods, company_ticker, date, debug_mode)
    most_recent_income_statements_for_this_date = get_most_recent_income_statement_for_given_company_for_given_date_company_outlook_n_periods(number_of_periods, company_ticker, date, debug_mode)
    if most_recent_income_statements_for_this_date == []:
        print("ERROR: Empty list.")
        return None
    else:
        average_attribute_of_decision_value = 0.0
        for income_statement in most_recent_income_statements_for_this_date:

            # Todo: Refactor
            index_of_amount_of_shares = 4
            decision_value = income_statement[attribute_of_decision_index] / income_statement[index_of_amount_of_shares]
            average_attribute_of_decision_value = average_attribute_of_decision_value + decision_value

        average_attribute_of_decision_value = average_attribute_of_decision_value / len(most_recent_income_statements_for_this_date)

        # attributeOfdecision_value = most_recent_income_statements_for_this_date[0][attribute_of_decision_index]
        share_price_for_this_date = None
        date_variable = date

        # I want to try to increase 4 times, on 5th attempt - print error. The loop works in 0 - (n-1) range.
        AMOUNT_OF_DATE_INCREASE_TRIES = 4
        for i in range(0, (AMOUNT_OF_DATE_INCREASE_TRIES + 1)):
            share_price_for_this_date = read_db_share_price_in_particular_day(company_ticker, date_variable, debug_mode)
            if (share_price_for_this_date == None):
                date_variable = increase_date_by_day(date_variable, DATE_FORMAT, debug_mode)
            else:
                break

        investment_value = average_attribute_of_decision_value / share_price_for_this_date
        print_investment_value_calculations(company_ticker, average_attribute_of_decision_value, share_price_for_this_date, investment_value, debug_mode)
        return investment_value
