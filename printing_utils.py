def print_set_name(set_name):
    if set_name != None:
        print(set_name)
        print("")


def print_set_properties(set_name, whole_period_length, sub_period_length):
    if set_name != None:
        print(set_name)
    if whole_period_length != None:
        print("WHOLE PERIOD LENGTH: " + whole_period_length)
    print("SUB-PERIOD LENGTH: " + str(sub_period_length))


def print_empty_line():
    print("")


def print_company_name(company_name, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "COMPANY " + company_name)


def print_start_of_sub_period(sub_period_counter, sub_periods_amount, debug_mode):
    if debug_mode:
        print("")
        print("DEBUG LOG: " + "-------------- ")
        print("DEBUG LOG: " + "START OF NEW SUB-PERIOD NUMBER " + str(sub_period_counter) + "/" + str(sub_periods_amount))
        print("")


def print_end_of_sub_period(debug_mode):
    if debug_mode:
        print("")
        print("DEBUG LOG: " + "END OF SUB-PERIOD")
        print("DEBUG LOG: " + "-------------- ")
        print("")


def print_average_weight(average_weight, debug_mode):
    if debug_mode:
        print("")
        print("DEBUG LOG: AVERAGE WEIGHT (VALUE): " + str(average_weight))
        print("")


def print_money_after_change(money, debug_mode):
    if debug_mode:
        print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY: " + str(money))


def print_first_and_last_day_prices(first_day_price, last_day_price, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "FIRST DAY PRICE " + str(first_day_price))
        print("DEBUG LOG: " + "LAST DAY PRICE " + str(last_day_price))


def print_average_change_of_given_companies_in_given_period(average_change):
    print("AVERAGE CHANGE OF GIVEN COMPANIES IN GIVEN PERIOD " + "{0:.2%}".format(average_change))


def print_change_in_invested_money(change_in_invested_money, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "CHANGE IN INVESTED MONEY (given company) " + "{0:.2%}".format(change_in_invested_money))
        print("")


def print_api_data_fetched(data, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "API DATA FETCHED: ")
        print(data)


def print_money_after_all_changes_according_to_my_strategy(money, debug_mode):
    if (debug_mode):
        print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY: " + str(money))


def print_money_after_all_changes_according_to_my_strategy_as_percentage(money_after_changes_as_percentage):
    print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY AS A PERCENTAGE: " + "{0:.2%}".format(money_after_changes_as_percentage))


def print_my_strategy_minus_average_change(my_strategy_to_average):
    print("MY STRATEGY - AVERAGE CHANGE: "+ "{0:.2%}".format(my_strategy_to_average))


def print_change_in_price(change_in_price, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "CHANGE IN PRICE " + "{0:.2%}".format(change_in_price))


def print_change_in_invested_money_for_all_given_companies_in_given_period(sum_of_changes_in_invested_money, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "CHANGE IN INVESTED MONEY (all given companies) IN GIVEN PERIOD " + "{0:.2%}".format(sum_of_changes_in_invested_money))
        print("")


def print_error_saving_into_database(sql_query, data, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "ERROR: RECORD HAS NOT BEEN SAVED INTO DATABASE")
        #Todo: Test printing of sqlQuery and str(data).
        print("DEBUG LOG: " + sql_query)
        print("DEBUG LOG: " + str(data))


def print_recalculated_normalized_weight(company_ticker, normalized_weight, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "RECALCULATED NORMALIZED WEIGHT " + company_ticker + " " + str(normalized_weight))


def print_investment_value_calculations(company_ticker, attribute_of_decision_value, share_price_for_this_date, investment_value, debug_mode):
    if debug_mode:
        print("")
        print("DEBUG LOG: " + "COMPANY " + company_ticker)
        print("DEBUG LOG: " + "ATTRIBUTE DECISION VALUE " + str(attribute_of_decision_value))
        print("DEBUG LOG: " + "SHARE PRICE FOR THIS DATE " + str(share_price_for_this_date))
        print("DEBUG LOG: " + "CALCULATED INVESTMENT VALUE " + str(investment_value))


def print_normalized_weight(company_ticker, normalized_weight, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "NORMALIZED WEIGHT " + company_ticker + " " + str(normalized_weight))
