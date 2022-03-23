import sqlite3 as sl
from DateUtils import increaseDateByDay
from DatabaseUtils import readDbSharePriceInParticularDay, readSharePricesPerParticularPeriod, tryToFetchPricesInParticularPeriod, getMostRecentIncomeStatementForGivenCompanyForGivenDate, getMostRecentIncomeStatementForGivenCompanyForGivenDate_nPeriods, getMostRecentIncomeStatementForGivenCompanyForGivenDate_companyOutlook_nPeriods
from Constants import DATE_FORMAT
from PrintingUtils import printCompanyName, printAverageWeight, printRecalculatedNormalizedWeight, printInvestmentValueCalculations, printNormalizedWeight

INVESTMENT_VALUE_NUMBER_OF_PERIODS = 4


def getWeightsForBetsForGivenCompaniesForGivenDate(companies, attributeOfDecisionIndex, givenDate, debugMode):
    calculateAverageInvestmentValueInThisDateForGivenCompanies(companies, attributeOfDecisionIndex, givenDate, debugMode)
    return getWeightsForBetsForGivenCompaniesForGivenDate_betThatOverpricedWillDropAndUnderpricedWillRaise(companies, attributeOfDecisionIndex, givenDate, debugMode)


def calculateAverageInvestmentValueInThisDateForGivenCompanies(companies, attributeOfDecisionIndex, givenDate, debugMode):
    sumOfInvestmentValues = 0.0
    result = "" + givenDate
    for companyTicker in companies:
        investmentValue = getInvestmentValueForGivenCompanyForGivenDate_nPeriods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, companyTicker, attributeOfDecisionIndex, givenDate, debugMode)
        sumOfInvestmentValues = sumOfInvestmentValues + investmentValue
        result = result + " " + str(investmentValue)
    averageInvestmentValue = sumOfInvestmentValues / len(companies)
    result = result + " " + str(averageInvestmentValue)
    print(result)


# New approach
def getWeightsForBetsForGivenCompaniesForGivenDate_betThatOverpricedWillDropAndUnderpricedWillRaise(companies, attributeOfDecisionIndex, givenDate, debugMode):
    calculatedWeights = []
    normalizedWeights = []
    sumOfWeights = 0.0

    for companyTicker in companies:
        weight = getInvestmentValueForGivenCompanyForGivenDate_nPeriods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, companyTicker, attributeOfDecisionIndex, givenDate, debugMode)

        if (weight > 0):
            calculatedWeights.append((companyTicker, weight))
            sumOfWeights = sumOfWeights + weight
        # else if (weight < 0):
        #     calculatedWeights.append((companyTicker, weight))
        #     sumOfWeights = sumOfWeights + (weight * -1)

    numberOfWeights = len(calculatedWeights)
    averageWeight = sumOfWeights / numberOfWeights
    reCalculatedWeights = []
    sumOfRecalculatedWeights = 0.0
    for weight in calculatedWeights:
        companyTicker = weight[0]
        weightValue = weight[1]
        # Only positive numbers
        reCalculatedWeight = weightValue - averageWeight
        reCalculatedWeights.append((companyTicker, reCalculatedWeight))
        if reCalculatedWeight > 0:
            sumOfRecalculatedWeights += reCalculatedWeight
        if reCalculatedWeight < 0:
            sumOfRecalculatedWeights += (reCalculatedWeight * -1)

    printAverageWeight(averageWeight, debugMode)

    for weight in reCalculatedWeights:
        companyTicker = weight[0]
        weightValue = weight[1]

        normalizedWeight = weightValue / sumOfRecalculatedWeights
        normalizedWeights.append((companyTicker, normalizedWeight))
        printRecalculatedNormalizedWeight(companyTicker, normalizedWeight, debugMode)

    return normalizedWeights


# Old approach - not sure if still works!
def getWeightsForBetsForGivenCompaniesForGivenDate_buyAllJustLessOfOverpricedAndMoreOfUnderpriced(companies, attributeOfDecisionIndex, givenDate, debugMode):
    calculatedWeights = []
    normalizedWeights = []
    sumOfWeights = 0.0

    for companyTicker in companies:
        weight = getInvestmentValueForGivenCompanyForGivenDate_nPeriods(INVESTMENT_VALUE_NUMBER_OF_PERIODS, companyTicker, attributeOfDecisionIndex, givenDate, debugMode)

        if (weight > 0):
            calculatedWeights.append((companyTicker, weight))
            sumOfWeights = sumOfWeights + weight
        # else if (weight < 0):
        #     calculatedWeights.append((companyTicker, weight))
        #     sumOfWeights = sumOfWeights + (weight * -1)

    for weight in calculatedWeights:
        companyTicker = weight[0]
        weightValue = weight[1]

        if (weightValue > 0):
            normalizedWeight = weightValue / sumOfWeights
            normalizedWeights.append((companyTicker, normalizedWeight))
            printNormalizedWeight(companyTicker, normalizedWeight, debugMode)
        # else if (weightValue < 0):

    return normalizedWeights


def getInvestmentValueForGivenCompanyForGivenDate_nPeriods(numberOfPeriods, companyTicker, attributeOfDecisionIndex, date, debugMode = False):
    # mostRecentIncomeStatementsForThisDate = getMostRecentIncomeStatementForGivenCompanyForGivenDate_nPeriods(numberOfPeriods, companyTicker, date, debugMode)
    mostRecentIncomeStatementsForThisDate = getMostRecentIncomeStatementForGivenCompanyForGivenDate_companyOutlook_nPeriods(numberOfPeriods, companyTicker, date, debugMode)
    if mostRecentIncomeStatementsForThisDate == []:
        print("ERROR: Empty list.")
        return None
    else:
        averageAttributeOfDecisionValue = 0.0
        for incomeStatement in mostRecentIncomeStatementsForThisDate:

            # Todo: Refactor
            indexOfAmountOfShares = 4
            decisionValue = incomeStatement[attributeOfDecisionIndex] / incomeStatement[indexOfAmountOfShares]
            averageAttributeOfDecisionValue = averageAttributeOfDecisionValue + decisionValue

        averageAttributeOfDecisionValue = averageAttributeOfDecisionValue / len(mostRecentIncomeStatementsForThisDate)

        # attributeOfDecisionValue = mostRecentIncomeStatementsForThisDate[0][attributeOfDecisionIndex]
        sharePriceForThisDate = None
        date_variable = date

        # I want to try to increase 4 times, on 5th attempt - print error. The loop works in 0 - (n-1) range.
        AMOUNT_OF_DATE_INCREASE_TRIES = 4
        for i in range(0, (AMOUNT_OF_DATE_INCREASE_TRIES + 1)):
            sharePriceForThisDate = readDbSharePriceInParticularDay(companyTicker, date_variable, debugMode)
            if (sharePriceForThisDate == None):
                date_variable = increaseDateByDay(date_variable, DATE_FORMAT, debugMode)
            else:
                break

        investmentValue = averageAttributeOfDecisionValue / sharePriceForThisDate
        printInvestmentValueCalculations(companyTicker, averageAttributeOfDecisionValue, sharePriceForThisDate, investmentValue, debugMode)
        return investmentValue
