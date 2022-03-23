from printing_utils import printSetProperties, printEmptyLine, printStartOfSubperiod, printEndOfSubperiod, printMoneyAfterChange, printMoneyAfterAllChangesAccordingToMyStrategy, printMoneyAfterAllChangesAccordingToMyStrategyAsPercentage, printMyStrategyMinusaverage_change
from calculation_utils import calculate_change_for_bets_made_for_given_companies_in_particular_period, calculate_average_change_for_given_companies_in_particular_period
from date_utils import split_whole_period_into_chunks
from api_utils import fetch_share_prices_from_the_api, fetch_company_outlook_from_the_api
from database_utils import initialize_database, save_fetched_data_into_database_share_prices, read_all_data_from_database, save_fetched_data_into_database_company_outlook
from saving_to_txt_utils import writeResultIntoTxtLog_set_name, writeResultIntoTxtLog_periods, writeResultIntoTxtLog_results
from constants import DATE_FORMAT, COMPANIES_TICKERS_TEST, COMPANIES_TICKERS_TEST_2, XXX, COMPANIES_TICKERS_BIG_THREE, COMPANIES_TICKERS_BIG_FOUR, COMPANIES_TICKERS_TESLA, COMPANIES_TICKERS_TESLA_APPLE, COMPANIES_TICKERS_MULTISET
from weights_factory import getWeightsForBetsForGivenCompaniesForGivenDate


COMPANIES_SET = XXX

SHARE_PRICES_FETCHING_START_DATE = '2021-03-01'
SHARE_PRICES_FETCHING_END_DATE = '2022-03-01'

START_DATE = '2021-03-01'
END_DATE = '2022-03-01'

SUBPERIOD_LENGTH_IN_DAYS_ARRAY = [10]


ATTRIBUTE_OF_DECISION_INDEX = 3
OUTPUT_DIRECTORY = "results_output/"


def run_multiple_simulations(companies, start_date, end_date, attributeOfDecisionIndex, wholePeriodLength, sub_period_length_in_daysArray, set_name = None, debug_mode = False):
    for sub_period_length_in_days in sub_period_length_in_daysArray:
        runMultiplePeriodSimulation(companies, start_date, end_date, attributeOfDecisionIndex, wholePeriodLength, sub_period_length_in_days, set_name, debug_mode)


def runMultiplePeriodSimulation(companies, start_date, end_date, attributeOfDecisionIndex, wholePeriodLength, periodLengthInDays, set_name = None, debug_mode = False):
    printEmptyLine()
    printSetProperties(set_name, wholePeriodLength, periodLengthInDays)

    writeResultIntoTxtLog_set_name(OUTPUT_DIRECTORY, set_name)
    writeResultIntoTxtLog_periods(OUTPUT_DIRECTORY, wholePeriodLength, periodLengthInDays)

    originalMoney = 1000
    money = originalMoney

    # 1. Split the whole period into chunks.
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, periodLengthInDays, DATE_FORMAT, debug_mode)

    # 2. Calculate weights for each chunk, and then change in invested money using gathered weights.
    # 3. Sum up all the chunks results and display.
    subPeriodCounter = 0
    sub_periods_amount = len(sub_period_dates)
    for subPeriod in sub_period_dates:

        subPeriodCounter = subPeriodCounter + 1

        printStartOfSubperiod(subPeriodCounter, sub_periods_amount, debug_mode)

        subPeriodWeights = getWeightsForBetsForGivenCompaniesForGivenDate(companies, attributeOfDecisionIndex, subPeriod[0], debug_mode)

        is_it_last_sub_period = False
        if (subPeriod[1] == end_date):
            is_it_last_sub_period = True

        investmentChangeInThisSubPeriod = calculate_change_for_bets_made_for_given_companies_in_particular_period(subPeriodWeights, is_it_last_sub_period, subPeriod[0], subPeriod[1], set_name, debug_mode)
        money = money * (1 + investmentChangeInThisSubPeriod)

        printMoneyAfterChange(money, debug_mode)
        printEndOfSubperiod(debug_mode)

    printMoneyAfterAllChangesAccordingToMyStrategy(money, debug_mode)

    moneyAfterChangesAsPercentage  = (money - originalMoney)/ originalMoney
    printMoneyAfterAllChangesAccordingToMyStrategyAsPercentage(moneyAfterChangesAsPercentage)

    # 4. Check the real average change for comparison.
    average_change = calculate_average_change_for_given_companies_in_particular_period(companies, start_date, end_date, set_name, debug_mode)
    myStrategyToAverage  = moneyAfterChangesAsPercentage - average_change
    printMyStrategyMinusaverage_change(myStrategyToAverage)

    writeResultIntoTxtLog_results(OUTPUT_DIRECTORY, moneyAfterChangesAsPercentage, average_change)

    # Final line
    printEmptyLine()


def fetchNecessaryDataForExperiment(companies):
    initialize_database()

    data = fetch_company_outlook_from_the_api(companies)
    save_fetched_data_into_database_company_outlook(data, False)

    # data = fetch_income_statements_from_the_api(companies)
    # save_fetched_data_into_database_income_statements(data, False)

    sharePricesData = fetch_share_prices_from_the_api(companies, SHARE_PRICES_FETCHING_START_DATE, SHARE_PRICES_FETCHING_END_DATE)
    save_fetched_data_into_database_share_prices(sharePricesData, DATE_FORMAT, False)

    read_all_data_from_database()


# Main App
fetchNecessaryDataForExperiment(COMPANIES_SET)
run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, ATTRIBUTE_OF_DECISION_INDEX, None, SUBPERIOD_LENGTH_IN_DAYS_ARRAY, "TESTING SET", False)
