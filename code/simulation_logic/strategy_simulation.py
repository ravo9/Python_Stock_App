from .calculation_utils import calculate_investment_value_change, calculate_average_share_price_change_for_given_companies_in_given_period, calculate_weights
from .date_utils import split_whole_period_into_chunks

def run_multiple_simulations(companies, start_date, end_date, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY):
    for sub_period_length in SUB_PERIOD_LENGTH_IN_DAYS_ARRAY:
        for number_of_reports_for_calculation in NUMBER_OF_REPORTS_TAKEN_FOR_CALCULATION_ARRAY:
            _run_simulation(companies, start_date, end_date, sub_period_length, number_of_reports_for_calculation)

def _run_simulation(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation):
    # Get back in time. Invest given money (e.g. $100) in given companies equally ($100 each) - tested manually on paper.
    change_in_value_of_money_invested_equally = calculate_average_share_price_change_for_given_companies_in_given_period(companies, start_date, end_date)
    # Get back in time. Invest given money given companies not equally, but accordingly to the tested strategy (expressed by bets/ weights values).
    change_in_value_of_money_invested_by_using_tested_strategy = _perform_simulation_logic(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation)
    _present_simulation_results(change_in_value_of_money_invested_equally, change_in_value_of_money_invested_by_using_tested_strategy)
    return change_in_value_of_money_invested_by_using_tested_strategy # Used by otimisation.

def _perform_simulation_logic(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation, original_money = 1000):
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days)
    money = original_money
    for index, (sub_period_start_date, sub_period_end_date) in enumerate(sub_period_dates):
        _display_progress(index + 1, len(sub_period_dates))
        sub_period_weights = calculate_weights(companies, sub_period_start_date, number_of_reports_for_calculation)
        # if index != 0:
        #     sub_period_weights = modify_weights(sub_period_weights, start_date, sub_period_end_date, period_length_in_days, number_of_reports_for_calculation)
        investment_change = calculate_investment_value_change(sub_period_weights, sub_period_start_date, sub_period_end_date)
        money *= (1 + investment_change)
    return (money - original_money)/ original_money

def modify_weights(sub_period_weights, start_date, end_date, period_length_in_days, number_of_reports_for_calculation):
    modified_weights = []
    for ticker, weight in sub_period_weights:
        average_value_this_company_is_traded_per_one_dollar = calculate_average_market_value_per_dollar([ticker], start_date, end_date, period_length_in_days, number_of_reports_for_calculation)
        modified_weight = float(weight)/float(average_value_this_company_is_traded_per_one_dollar)
        modified_weight -= float(1)
        modified_weights.append((ticker, float(modified_weight)))
    return modified_weights

def calculate_average_market_value_per_dollar(companies, start_date, end_date, period_length_in_days, number_of_reports_for_calculation):
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days)
    average_value_per_dollar_spent_across_sub_periods = 0.0
    acc = 1
    for sub_period_start_date, sub_period_end_date in sub_period_dates:
        _display_progress(acc, len(sub_period_dates))
        acc += 1
        sub_period_weights = calculate_weights(companies, sub_period_start_date, number_of_reports_for_calculation)
        for ticker, value_per_dollar_spent in sub_period_weights: print(f"Average value per dollar spent for {ticker} on {sub_period_start_date} : {value_per_dollar_spent}")
        average_value = sum(value for ticker, value in sub_period_weights) / len(sub_period_weights)
        if sub_period_weights: print(f"Average value per dollar spent for given companies on {sub_period_start_date} : {average_value}\n")
        average_value_per_dollar_spent_across_sub_periods += average_value
    print("AVERAGE VALUE PER DOLLAR SPENT ACROSS WHOLE PERIOD: " + str(average_value_per_dollar_spent_across_sub_periods/len(sub_period_dates)))
    return average_value_per_dollar_spent_across_sub_periods/len(sub_period_dates)

def _display_progress(acc, total_length): print(f"{((acc/total_length) * 100):.2f}%", end='\r')

def _present_simulation_results(money_invested_equally, money_invested_according_to_strategy):
    print("MONEY INVESTED IN GIVEN COMPANIES EQUALLY (AVERAGE): " + "{0:.2%}".format(money_invested_equally))
    print("MONEY INVESTED IN GIVEN COMPANIES USING TESTED STRATEGY: " + "{0:.2%}".format(money_invested_according_to_strategy))
