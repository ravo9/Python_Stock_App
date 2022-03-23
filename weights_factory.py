import sqlite3 as sl
from date_utils import increase_date_by_day
from database_utils import read_db_share_price_in_particular_day, read_share_prices_per_particular_period, try_to_fetch_prices_in_particular_period, get_most_recent_income_statement_for_given_company_for_given_date, get_most_recent_income_statement_for_given_company_for_given_date_n_periods, get_most_recent_income_statement_for_given_company_for_given_date_company_outlook_n_periods
from constants import DATE_FORMAT
from printing_utils import print_company_name, printAverageWeight, printRecalculatedNormalizedWeight, printInvestmentValueCalculations, printNormalizedWeight

INVESTMENT_VALUE_NUMBER_OF_PERIODS = 4


def getWeightsForBetsForGivenCompaniesForGivenDate(companies, attributeOfDecisionIndex, givenDate, debug_mode):
    calculateAverageInvestmentValueInThisDateForGivenCompanies(companies, attributeOfDecisionIndex, givenDate, debug_mode)
    return getWeightsForBetsForGivenCompaniesForGivenDate_betThatOverpricedWillDropAndUnderpricedWillRaise(companies, attributeOfDecisionIndex, givenDate, debug_mode)


def calculateAverageInvestmentValueInThisDateForGivenCompanies(companies, attributeOfDecisionIndex, givenDate, debug_mode):
    sumOfInvestmentValues = 0.0
    result = "" + givenDate
    for company_ticker in companies:
        investmentValue = getInvestmentValueForGivenCompanyForGivenDate_nPeriods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attributeOfDecisionIndex, givenDate, debug_mode)
        sumOfInvestmentValues = sumOfInvestmentValues + investmentValue
        result = result + " " + str(investmentValue)
    averageInvestmentValue = sumOfInvestmentValues / len(companies)
    result = result + " " + str(averageInvestmentValue)
    print(result)


# New approach
def getWeightsForBetsForGivenCompaniesForGivenDate_betThatOverpricedWillDropAndUnderpricedWillRaise(companies, attributeOfDecisionIndex, givenDate, debug_mode):
    calculatedWeights = []
    normalizedWeights = []
    sumOfWeights = 0.0

    for company_ticker in companies:
        weight = getInvestmentValueForGivenCompanyForGivenDate_nPeriods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attributeOfDecisionIndex, givenDate, debug_mode)

        if (weight > 0):
            calculatedWeights.append((company_ticker, weight))
            sumOfWeights = sumOfWeights + weight
        # else if (weight < 0):
        #     calculatedWeights.append((company_ticker, weight))
        #     sumOfWeights = sumOfWeights + (weight * -1)

    numberOfWeights = len(calculatedWeights)
    averageWeight = sumOfWeights / numberOfWeights
    reCalculatedWeights = []
    sumOfRecalculatedWeights = 0.0
    for weight in calculatedWeights:
        company_ticker = weight[0]
        weightValue = weight[1]
        # Only positive numbers
        reCalculatedWeight = weightValue - averageWeight
        reCalculatedWeights.append((company_ticker, reCalculatedWeight))
        if reCalculatedWeight > 0:
            sumOfRecalculatedWeights += reCalculatedWeight
        if reCalculatedWeight < 0:
            sumOfRecalculatedWeights += (reCalculatedWeight * -1)

    printAverageWeight(averageWeight, debug_mode)

    for weight in reCalculatedWeights:
        company_ticker = weight[0]
        weightValue = weight[1]

        normalizedWeight = weightValue / sumOfRecalculatedWeights
        normalizedWeights.append((company_ticker, normalizedWeight))
        printRecalculatedNormalizedWeight(company_ticker, normalizedWeight, debug_mode)

    return normalizedWeights


# Old approach - not sure if still works!
def getWeightsForBetsForGivenCompaniesForGivenDate_buyAllJustLessOfOverpricedAndMoreOfUnderpriced(companies, attributeOfDecisionIndex, givenDate, debug_mode):
    calculatedWeights = []
    normalizedWeights = []
    sumOfWeights = 0.0

    for company_ticker in companies:
        weight = getInvestmentValueForGivenCompanyForGivenDate_nPeriods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, company_ticker, attributeOfDecisionIndex, givenDate, debug_mode)

        if (weight > 0):
            calculatedWeights.append((company_ticker, weight))
            sumOfWeights = sumOfWeights + weight
        # else if (weight < 0):
        #     calculatedWeights.append((company_ticker, weight))
        #     sumOfWeights = sumOfWeights + (weight * -1)

    for weight in calculatedWeights:
        company_ticker = weight[0]
        weightValue = weight[1]

        if (weightValue > 0):
            normalizedWeight = weightValue / sumOfWeights
            normalizedWeights.append((company_ticker, normalizedWeight))
            printNormalizedWeight(company_ticker, normalizedWeight, debug_mode)
        # else if (weightValue < 0):

    return normalizedWeights


def getInvestmentValueForGivenCompanyForGivenDate_nPeriods(number_of_periods, company_ticker, attributeOfDecisionIndex, date, debug_mode = False):
    # most_recent_income_statements_for_this_date = get_most_recent_income_statement_for_given_company_for_given_date_n_periods(number_of_periods, company_ticker, date, debug_mode)
    most_recent_income_statements_for_this_date = get_most_recent_income_statement_for_given_company_for_given_date_company_outlook_n_periods(number_of_periods, company_ticker, date, debug_mode)
    if most_recent_income_statements_for_this_date == []:
        print("ERROR: Empty list.")
        return None
    else:
        averageAttributeOfDecisionValue = 0.0
        for incomeStatement in most_recent_income_statements_for_this_date:

            # Todo: Refactor
            indexOfAmountOfShares = 4
            decisionValue = incomeStatement[attributeOfDecisionIndex] / incomeStatement[indexOfAmountOfShares]
            averageAttributeOfDecisionValue = averageAttributeOfDecisionValue + decisionValue

        averageAttributeOfDecisionValue = averageAttributeOfDecisionValue / len(most_recent_income_statements_for_this_date)

        # attributeOfDecisionValue = most_recent_income_statements_for_this_date[0][attributeOfDecisionIndex]
        sharePriceForThisDate = None
        date_variable = date

        # I want to try to increase 4 times, on 5th attempt - print error. The loop works in 0 - (n-1) range.
        AMOUNT_OF_DATE_INCREASE_TRIES = 4
        for i in range(0, (AMOUNT_OF_DATE_INCREASE_TRIES + 1)):
            sharePriceForThisDate = read_db_share_price_in_particular_day(company_ticker, date_variable, debug_mode)
            if (sharePriceForThisDate == None):
                date_variable = increase_date_by_day(date_variable, DATE_FORMAT, debug_mode)
            else:
                break

        investmentValue = averageAttributeOfDecisionValue / sharePriceForThisDate
        printInvestmentValueCalculations(company_ticker, averageAttributeOfDecisionValue, sharePriceForThisDate, investmentValue, debug_mode)
        return investmentValue
