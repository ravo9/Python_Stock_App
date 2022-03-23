import pandas_datareader as web
import datetime
import sqlite3 as sl

from PrintingUtils import printSetName, printSetProperties, printEmptyLine, printStartOfSubperiod, printEndOfSubperiod, printMoneyAfterChange, printMoneyAfterAllChangesAccordingToMyStrategy, printMoneyAfterAllChangesAccordingToMyStrategyAsPercentage, printMyStrategyMinusAverageChange
from CalculationUtils import calculateChangeInSharePrice, calculateChangeInInvestedMoney, calculateChangeForBetsMadeForGivenCompaniesInParticularPeriod, calculateAverageChangeForGivenCompaniesInParticularPeriod
from DateUtils import splitWholePeriodIntoChunks
from ApiUtils import fetchDataFromApi, fetchIncomeStatementsFromTheApi, fetchSharePricesFromTheApi, fetchCompanyOutlookFromTheApi
from DatabaseUtils import initializeDatabase, saveFetchedDataIntoDatabase_incomeStatements, saveFetchedDataIntoDatabase_sharePrices, readAllDataFromDatabase, saveFetchedDataIntoDatabase_companyOutlook
from SavingToTxtUtils import writeResultIntoTxtLog_setName, writeResultIntoTxtLog_periods, writeResultIntoTxtLog_results
from Constants import DATE_FORMAT, COMPANIES_TICKERS_TEST, COMPANIES_TICKERS_TEST_2, XXX, COMPANIES_TICKERS_BIG_THREE, COMPANIES_TICKERS_BIG_FOUR, COMPANIES_TICKERS_TESLA, COMPANIES_TICKERS_TESLA_APPLE, COMPANIES_TICKERS_MULTISET
from WeightsFactory import getWeightsForBetsForGivenCompaniesForGivenDate


COMPANIES_SET = COMPANIES_TICKERS_TEST_2

SHARE_PRICES_FETCHING_START_DATE = '2021-03-01'
SHARE_PRICES_FETCHING_END_DATE = '2022-03-01'

START_DATE = '2021-03-01'
END_DATE = '2022-03-01'

SUBPERIOD_LENGTH_IN_DAYS_ARRAY = [10]


ATTRIBUTE_OF_DECISION_INDEX = 3
OUTPUT_DIRECTORY = "results_output/"


def runMultipleSimulations(companies, startDate, endDate, attributeOfDecisionIndex, wholePeriodLength, subPeriodLengthInDaysArray, setName = None, debugMode = False):
    for subPeriodLengthInDays in subPeriodLengthInDaysArray:
        runMultiplePeriodSimulation(companies, startDate, endDate, attributeOfDecisionIndex, wholePeriodLength, subPeriodLengthInDays, setName, debugMode)


def runMultiplePeriodSimulation(companies, startDate, endDate, attributeOfDecisionIndex, wholePeriodLength, periodLengthInDays, setName = None, debugMode = False):
    printEmptyLine()
    printSetProperties(setName, wholePeriodLength, periodLengthInDays)

    writeResultIntoTxtLog_setName(OUTPUT_DIRECTORY, setName)
    writeResultIntoTxtLog_periods(OUTPUT_DIRECTORY, wholePeriodLength, periodLengthInDays)

    originalMoney = 1000
    money = originalMoney

    # 1. Split the whole period into chunks.
    subPeriodDates = splitWholePeriodIntoChunks(startDate, endDate, periodLengthInDays, DATE_FORMAT, debugMode)

    # 2. Calculate weights for each chunk, and then change in invested money using gathered weights.
    # 3. Sum up all the chunks results and display.
    subPeriodCounter = 0
    subPeriodsAmount = len(subPeriodDates)
    for subPeriod in subPeriodDates:

        subPeriodCounter = subPeriodCounter + 1

        printStartOfSubperiod(subPeriodCounter, subPeriodsAmount, debugMode)

        subPeriodWeights = getWeightsForBetsForGivenCompaniesForGivenDate(companies, attributeOfDecisionIndex, subPeriod[0], debugMode)

        isItLastSubPeriod = False
        if (subPeriod[1] == endDate):
            isItLastSubPeriod = True

        investmentChangeInThisSubPeriod = calculateChangeForBetsMadeForGivenCompaniesInParticularPeriod(subPeriodWeights, isItLastSubPeriod, subPeriod[0], subPeriod[1], setName, debugMode)
        money = money * (1 + investmentChangeInThisSubPeriod)

        printMoneyAfterChange(money, debugMode)
        printEndOfSubperiod(debugMode)

    printMoneyAfterAllChangesAccordingToMyStrategy(money, debugMode)

    moneyAfterChangesAsPercentage  = (money - originalMoney)/ originalMoney
    printMoneyAfterAllChangesAccordingToMyStrategyAsPercentage(moneyAfterChangesAsPercentage)

    # 4. Check the real average change for comparison.
    averageChange = calculateAverageChangeForGivenCompaniesInParticularPeriod(companies, startDate, endDate, setName, debugMode)
    myStrategyToAverage  = moneyAfterChangesAsPercentage - averageChange
    printMyStrategyMinusAverageChange(myStrategyToAverage)

    writeResultIntoTxtLog_results(OUTPUT_DIRECTORY, moneyAfterChangesAsPercentage, averageChange)

    # Final line
    printEmptyLine()


def fetchNecessaryDataForExperiment(companies):
    initializeDatabase()

    data = fetchCompanyOutlookFromTheApi(companies)
    saveFetchedDataIntoDatabase_companyOutlook(data, False)

    # data = fetchIncomeStatementsFromTheApi(companies)
    # saveFetchedDataIntoDatabase_incomeStatements(data, False)

    sharePricesData = fetchSharePricesFromTheApi(companies, SHARE_PRICES_FETCHING_START_DATE, SHARE_PRICES_FETCHING_END_DATE)
    saveFetchedDataIntoDatabase_sharePrices(sharePricesData, DATE_FORMAT, False)

    readAllDataFromDatabase()


# Main App
# fetchNecessaryDataForExperiment(COMPANIES_SET)
runMultipleSimulations(COMPANIES_SET, START_DATE, END_DATE, ATTRIBUTE_OF_DECISION_INDEX, None, SUBPERIOD_LENGTH_IN_DAYS_ARRAY, "TESTING SET", False)
