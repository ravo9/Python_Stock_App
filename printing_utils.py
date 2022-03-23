def print_set_name(set_name):
    if (set_name != None):
        print(set_name)
        print("")


def printSetProperties(set_name, wholePeriodLength, subPeriodLength):
    if (set_name != None):
        print(set_name)
    if (wholePeriodLength != None):
        print("WHOLE PERIOD LENGTH: " + wholePeriodLength)
    print("SUB-PERIOD LENGTH: " + str(subPeriodLength))


def printEmptyLine():
    print("")


def print_company_name(companyName, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "COMPANY " + companyName)


def printStartOfSubperiod(subPeriodCounter, sub_periods_amount, debug_mode):
    if (debug_mode):
        print("")
        print("DEBUG LOG: " + "-------------- ")
        print("DEBUG LOG: " + "START OF NEW SUB-PERIOD NUMBER " + str(subPeriodCounter) + "/" + str(sub_periods_amount))
        print("")


def printEndOfSubperiod(debug_mode):
    if (debug_mode):
        print("")
        print("DEBUG LOG: " + "END OF SUB-PERIOD")
        print("DEBUG LOG: " + "-------------- ")
        print("")


def printAverageWeight(averageWeight, debug_mode):
    if (debug_mode):
        print("")
        print("DEBUG LOG: AVERAGE WEIGHT (VALUE): " + str(averageWeight))
        print("")


def printMoneyAfterChange(money, debug_mode):
    if (debug_mode):
        print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY: " + str(money))


def print_first_and_last_day_prices(first_day_price, last_day_price, debug_mode):
    if (debug_mode):
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


def printMoneyAfterAllChangesAccordingToMyStrategy(money, debug_mode):
    if (debug_mode):
        print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY: " + str(money))


def printMoneyAfterAllChangesAccordingToMyStrategyAsPercentage(moneyAfterChangesAsPercentage):
    print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY AS A PERCENTAGE: " + "{0:.2%}".format(moneyAfterChangesAsPercentage))


def printMyStrategyMinusaverage_change(myStrategyToAverage):
    print("MY STRATEGY - AVERAGE CHANGE: "+ "{0:.2%}".format(myStrategyToAverage))


def print_change_in_price(change_in_price, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "CHANGE IN PRICE " + "{0:.2%}".format(change_in_price))


def print_change_in_invested_money_for_all_given_companies_in_given_period(sum_of_changes_in_invested_money, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "CHANGE IN INVESTED MONEY (all given companies) IN GIVEN PERIOD " + "{0:.2%}".format(sum_of_changes_in_invested_money))
        print("")


def print_error_saving_into_database(sqlQuery, data, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "ERROR: RECORD HAS NOT BEEN SAVED INTO DATABASE")
        #Todo: Test printing of sqlQuery and str(data).
        print("DEBUG LOG: " + sqlQuery)
        print("DEBUG LOG: " + str(data))


def printRecalculatedNormalizedWeight(company_ticker, normalizedWeight, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "RECALCULATED NORMALIZED WEIGHT " + company_ticker + " " + str(normalizedWeight))


def printInvestmentValueCalculations(company_ticker, attributeOfDecisionValue, sharePriceForThisDate, investmentValue, debug_mode):
    if (debug_mode):
        print("")
        print("DEBUG LOG: " + "COMPANY " + company_ticker)
        print("DEBUG LOG: " + "ATTRIBUTE DECISION VALUE " + str(attributeOfDecisionValue))
        print("DEBUG LOG: " + "SHARE PRICE FOR THIS DATE " + str(sharePriceForThisDate))
        print("DEBUG LOG: " + "CALCULATED INVESTMENT VALUE " + str(investmentValue))


def printNormalizedWeight(company_ticker, normalizedWeight, debug_mode):
    if (debug_mode):
        print("DEBUG LOG: " + "NORMALIZED WEIGHT " + company_ticker + " " + str(normalizedWeight))
