def print_simulation_results(money_after_changes_as_percentage, average_change, my_strategy_to_average):
    print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY AS A PERCENTAGE: " + "{0:.2%}".format(money_after_changes_as_percentage))
    print("AVERAGE CHANGE OF GIVEN COMPANIES IN GIVEN PERIOD " + "{0:.2%}".format(average_change))
    print("MY STRATEGY - AVERAGE CHANGE: "+ "{0:.2%}".format(my_strategy_to_average))

def print_empty_line():
    print("")

def print_company_name(company_name, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "COMPANY " + company_name)

def print_start_of_sub_period(sub_period_counter, sub_periods_amount, debug_mode):
    if debug_mode:
        print("")
        print("DEBUG LOG: " + "-------------- ")
        print("DEBUG LOG: " + "START OF NEW SUB-PERIOD NUMBER " + str(sub_period_counter) + "/" + str(sub_periods_amount))
        print("")

def print_first_and_last_day_prices(first_day_price, last_day_price, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "FIRST DAY PRICE " + str(first_day_price))
        print("DEBUG LOG: " + "LAST DAY PRICE " + str(last_day_price))

def print_change_in_invested_money(change_in_invested_money, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "CHANGE IN INVESTED MONEY (given company) " + "{0:.2%}".format(change_in_invested_money))
        print("")

def print_api_data_fetched(data, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "API DATA FETCHED: ")
        print(data)

def print_change_in_invested_money_for_all_given_companies_in_given_period(sum_of_changes_in_invested_money, debug_mode):
    if debug_mode:
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
