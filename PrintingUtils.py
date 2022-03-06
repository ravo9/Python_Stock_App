def printSetName(setName):
    if (setName != None):
        print(setName)
        print("")


def printSetProperties(setName, wholePeriodLength, subPeriodLength):
    if (setName != None):
        print(setName)
    if (wholePeriodLength != None):
        print("WHOLE PERIOD LENGTH: " + wholePeriodLength)
    print("SUB-PERIOD LENGTH: " + str(subPeriodLength))


def printEmptyLine():
    print("")


def printCompanyName(companyName, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "COMPANY " + companyName)


def printStartOfSubperiod(subPeriodCounter, subPeriodsAmount, debugMode):
    if (debugMode):
        print("")
        print("DEBUG LOG: " + "-------------- ")
        print("DEBUG LOG: " + "START OF NEW SUB-PERIOD NUMBER " + str(subPeriodCounter) + "/" + str(subPeriodsAmount))
        print("")


def printEndOfSubperiod(debugMode):
    if (debugMode):
        print("")
        print("DEBUG LOG: " + "END OF SUB-PERIOD")
        print("DEBUG LOG: " + "-------------- ")
        print("")


def printAverageWeight(averageWeight, debugMode):
    if (debugMode):
        print("")
        print("DEBUG LOG: AVERAGE WEIGHT (VALUE): " + str(averageWeight))
        print("")


def printMoneyAfterChange(money, debugMode):
    if (debugMode):
        print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY: " + str(money))


def printFirstAndLastDayPrices(firstDayPrice, lastDayPrice, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "FIRST DAY PRICE " + str(firstDayPrice))
        print("DEBUG LOG: " + "LAST DAY PRICE " + str(lastDayPrice))


def printAverageChangeOfGivenCompaniesInGivenPeriod(averageChange):
    print("AVERAGE CHANGE OF GIVEN COMPANIES IN GIVEN PERIOD " + "{0:.2%}".format(averageChange))


def printChangeInInvestedMoney(changeInInvestedMoney, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "CHANGE IN INVESTED MONEY (given company) " + "{0:.2%}".format(changeInInvestedMoney))
        print("")


def printApiDataFetched(data, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "API DATA FETCHED: ")
        print(data)


def printMoneyAfterAllChangesAccordingToMyStrategy(money, debugMode):
    if (debugMode):
        print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY: " + str(money))


def printMoneyAfterAllChangesAccordingToMyStrategyAsPercentage(moneyAfterChangesAsPercentage):
    print("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY AS A PERCENTAGE: " + "{0:.2%}".format(moneyAfterChangesAsPercentage))


def printMyStrategyMinusAverageChange(myStrategyToAverage):
    print("MY STRATEGY - AVERAGE CHANGE: "+ "{0:.2%}".format(myStrategyToAverage))


def printChangeInPrice(changeInPrice, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "CHANGE IN PRICE " + "{0:.2%}".format(changeInPrice))


def printChangeInInvestedMoneyForAllGivenCompaniesInGivenPeriod(sumOfChangesInInvestedMoney, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "CHANGE IN INVESTED MONEY (all given companies) IN GIVEN PERIOD " + "{0:.2%}".format(sumOfChangesInInvestedMoney))
        print("")


def printErrorSavingIntoDatabase(sqlQuery, data, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "ERROR: RECORD HAS NOT BEEN SAVED INTO DATABASE")
        #Todo: Test printing of sqlQuery and str(data).
        print("DEBUG LOG: " + sqlQuery)
        print("DEBUG LOG: " + str(data))


def printRecalculatedNormalizedWeight(companyTicker, normalizedWeight, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "RECALCULATED NORMALIZED WEIGHT " + companyTicker + " " + str(normalizedWeight))


def printInvestmentValueCalculations(companyTicker, attributeOfDecisionValue, sharePriceForThisDate, investmentValue, debugMode):
    if (debugMode):
        print("")
        print("DEBUG LOG: " + "COMPANY " + companyTicker)
        print("DEBUG LOG: " + "ATTRIBUTE DECISION VALUE " + str(attributeOfDecisionValue))
        print("DEBUG LOG: " + "SHARE PRICE FOR THIS DATE " + str(sharePriceForThisDate))
        print("DEBUG LOG: " + "CALCULATED INVESTMENT VALUE " + str(investmentValue))


def printNormalizedWeight(companyTicker, normalizedWeight, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "NORMALIZED WEIGHT " + companyTicker + " " + str(normalizedWeight))
