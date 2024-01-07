from printing_utils import print_set_properties, print_empty_line, print_start_of_sub_period, print_end_of_sub_period, print_money_after_change, print_money_after_all_changes_according_to_my_strategy, print_money_after_all_changes_according_to_my_strategy_as_percentage, print_my_strategy_minus_average_change
from calculation_utils import calculate_change_for_bets_made_for_given_companies_in_particular_period, calculate_average_change_for_given_companies_in_particular_period
from date_utils import split_whole_period_into_chunks
from api_utils import fetch_share_prices_from_the_api, fetch_income_statements_from_the_api
from database_utils import initialize_database, save_fetched_data_into_database_share_prices, read_all_data_from_database, save_fetched_data_into_database_income_statements
from saving_to_txt_utils import write_result_into_txt_log_set_name, write_result_into_txt_log_periods, write_result_into_txt_log_results
from constants import DATE_FORMAT, COMPANIES_TICKERS_TEST, COMPANIES_TICKERS_TEST_2, COMPANIES_TICKERS_BIG_THREE, COMPANIES_TICKERS_BIG_FOUR, COMPANIES_TICKERS_TESLA, COMPANIES_TICKERS_TESLA_APPLE, COMPANIES_TICKERS_MULTISET
from weights_factory import get_weights_for_bets_for_given_companies_for_given_date


COMPANIES_SET = COMPANIES_TICKERS_TESLA

SHARE_PRICES_FETCHING_START_DATE = '2021-03-01'
SHARE_PRICES_FETCHING_END_DATE = '2022-03-01'

START_DATE = '2021-03-01'
END_DATE = '2022-03-01'

SUB_PERIOD_LENGTH_IN_DAYS_ARRAY = [10]


ATTRIBUTE_OF_DECISION_INDEX = 3
OUTPUT_DIRECTORY = "results_output/"


def run_multiple_simulations(companies, start_date, end_date, attribute_of_decision_index, whole_period_length, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, set_name = None, debug_mode = False):
    for sub_period_length_in_days in SUB_PERIOD_LENGTH_IN_DAYS_ARRAY:
        run_multiple_period_simulation(companies, start_date, end_date, attribute_of_decision_index, whole_period_length, sub_period_length_in_days, set_name, debug_mode)


def run_multiple_period_simulation(companies, start_date, end_date, attribute_of_decision_index, whole_period_length, period_length_in_days, set_name = None, debug_mode = False):
    print_empty_line()
    print_set_properties(set_name, whole_period_length, period_length_in_days)

    write_result_into_txt_log_set_name(OUTPUT_DIRECTORY, set_name)
    write_result_into_txt_log_periods(OUTPUT_DIRECTORY, whole_period_length, period_length_in_days)

    original_money = 1000
    money = original_money

    # 1. Split the whole period into chunks.
    sub_period_dates = split_whole_period_into_chunks(start_date, end_date, period_length_in_days, DATE_FORMAT, debug_mode)

    # 2. Calculate weights for each chunk, and then change in invested money using gathered weights.
    # 3. Sum up all the chunks results and display.
    sub_period_counter = 0
    sub_periods_amount = len(sub_period_dates)
    for sub_period in sub_period_dates:

        sub_period_counter = sub_period_counter + 1

        print_start_of_sub_period(sub_period_counter, sub_periods_amount, debug_mode)

        sub_period_weights = get_weights_for_bets_for_given_companies_for_given_date(companies, attribute_of_decision_index, sub_period[0], debug_mode)

        is_it_last_sub_period = False
        if sub_period[1] == end_date:
            is_it_last_sub_period = True

        investment_change_in_this_sub_period = calculate_change_for_bets_made_for_given_companies_in_particular_period(sub_period_weights, is_it_last_sub_period, sub_period[0], sub_period[1], set_name, debug_mode)
        money = money * (1 + investment_change_in_this_sub_period)

        print_money_after_change(money, debug_mode)
        print_end_of_sub_period(debug_mode)

    print_money_after_all_changes_according_to_my_strategy(money, debug_mode)

    money_after_changes_as_percentage  = (money - original_money)/ original_money
    print_money_after_all_changes_according_to_my_strategy_as_percentage(money_after_changes_as_percentage)

    # 4. Check the real average change for comparison.
    average_change = calculate_average_change_for_given_companies_in_particular_period(companies, start_date, end_date, set_name, debug_mode)
    my_strategy_to_average  = money_after_changes_as_percentage - average_change
    print_my_strategy_minus_average_change(my_strategy_to_average)

    write_result_into_txt_log_results(OUTPUT_DIRECTORY, money_after_changes_as_percentage, average_change)

    # Final line
    print_empty_line()


def fetch_necessary_data_for_experiment(companies):
    initialize_database()

    # Todo: Licence 29 USD required for these - find replacement.
    # data = fetch_company_outlook_from_the_api(companies)
    # save_fetched_data_into_database_company_outlook(data, False)
    # data = fetch_income_statements_from_the_api(companies)
    # save_fetched_data_into_database_income_statements(data, False)

    save_fetched_data_into_database_share_prices(
        fetch_share_prices_from_the_api(
            companies,
            SHARE_PRICES_FETCHING_START_DATE,
            SHARE_PRICES_FETCHING_END_DATE
        ),
        DATE_FORMAT,
        False
    )

    read_all_data_from_database()


# Main App
fetch_necessary_data_for_experiment(COMPANIES_SET)
# run_multiple_simulations(COMPANIES_SET, START_DATE, END_DATE, ATTRIBUTE_OF_DECISION_INDEX, None, SUB_PERIOD_LENGTH_IN_DAYS_ARRAY, "TESTING SET", False)
