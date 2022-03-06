import sqlite3 as sl
from DateUtils import increaseDateByDay
from DatabaseUtils import readDbSharePriceInParticularDay, readSharePricesPerParticularPeriod, tryToFetchPricesInParticularPeriod, getMostRecentIncomeStatementForGivenCompanyForGivenDate
from Constants import DATE_FORMAT
from PrintingUtils import printCompanyName, printFirstAndLastDayPrices, printAverageChangeOfGivenCompaniesInGivenPeriod, printChangeInInvestedMoney, printChangeInPrice, printChangeInInvestedMoneyForAllGivenCompaniesInGivenPeriod

def calculateChangeForBetsMadeForGivenCompaniesInParticularPeriod(companiesTickersWithWeights, isItLastSubPeriod, startDate, endDate, setName = None, debugMode = False):
    sumOfChangesInInvestedMoney = 0.0
    if (debugMode):
        print("")

    for companyWithWeight in companiesTickersWithWeights:
        companyTicker, companyBetWeight = companyWithWeight

        printCompanyName(companyTicker, debugMode)
        sharePricesTable = tryToFetchPricesInParticularPeriod(companyTicker, startDate, endDate, isItLastSubPeriod, debugMode)

        firstDayPrice = sharePricesTable[0][0]
        lastDayPrice = sharePricesTable[0][-1]

        printFirstAndLastDayPrices(firstDayPrice, lastDayPrice, debugMode)

        changeInPrice = calculateChangeInSharePrice(firstDayPrice, lastDayPrice, debugMode)
        changeInInvestedMoney = calculateChangeInInvestedMoney(changeInPrice, companyBetWeight, debugMode)
        sumOfChangesInInvestedMoney += changeInInvestedMoney

    printChangeInInvestedMoneyForAllGivenCompaniesInGivenPeriod(sumOfChangesInInvestedMoney, debugMode)

    return sumOfChangesInInvestedMoney


def calculateAverageChangeForGivenCompaniesInParticularPeriod(companiesTickers, startDate, endDate, setName = None, debugMode = False):
    sumOfChanges = 0.0
    amountOfCompanies = len(companiesTickers)
    if (debugMode):
        print("")

    for company in companiesTickers:
        printCompanyName(company, debugMode)

        sharePricesTable = tryToFetchPricesInParticularPeriod(company, startDate, endDate, True, debugMode)

        firstDayPrice = sharePricesTable[0][0]
        lastDayPrice = sharePricesTable[0][-1]

        printFirstAndLastDayPrices(firstDayPrice, lastDayPrice, debugMode)

        changeInPrice = calculateChangeInSharePrice(firstDayPrice, lastDayPrice, debugMode)
        sumOfChanges += changeInPrice

        if (debugMode):
            print("")

    averageChange = sumOfChanges / amountOfCompanies
    printAverageChangeOfGivenCompaniesInGivenPeriod(averageChange)
    return averageChange


def calculateChangeInSharePrice(firstDayPrice, lastDayPrice, debugMode):
    changeInPrice = (lastDayPrice - firstDayPrice)/firstDayPrice
    printChangeInPrice(changeInPrice, debugMode)
    return changeInPrice


def calculateChangeInInvestedMoney(changeInPrice, companyBetWeight, debugMode):
    changeInInvestedMoney = changeInPrice * companyBetWeight
    printChangeInInvestedMoney(changeInInvestedMoney, debugMode)
    return changeInInvestedMoney
