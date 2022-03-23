from database_utils import try_to_fetch_prices_in_particular_period
from printing_utils import print_company_name, print_first_and_last_day_prices, print_average_change_of_given_companies_in_given_period, print_change_in_invested_money, print_change_in_price, print_change_in_invested_money_for_all_given_companies_in_given_period

def calculate_change_for_bets_made_for_given_companies_in_particular_period(companies_tickers_with_weights, is_it_last_sub_period, start_date, end_date, set_name = None, debug_mode = False):
    sum_of_changes_in_invested_money = 0.0
    if (debug_mode):
        print("")

    for company_with_weight in companies_tickers_with_weights:
        company_ticker, company_bet_weight = company_with_weight

        print_company_name(company_ticker, debug_mode)
        share_prices_table = try_to_fetch_prices_in_particular_period(company_ticker, start_date, end_date, is_it_last_sub_period, debug_mode)

        first_day_price = share_prices_table[0][0]
        last_day_price = share_prices_table[0][-1]

        print_first_and_last_day_prices(first_day_price, last_day_price, debug_mode)

        change_in_price = calculate_change_in_share_price(first_day_price, last_day_price, debug_mode)
        change_in_invested_money = calculate_change_in_invested_money(change_in_price, company_bet_weight, debug_mode)
        sum_of_changes_in_invested_money += change_in_invested_money

    print_change_in_invested_money_for_all_given_companies_in_given_period(sum_of_changes_in_invested_money, debug_mode)

    return sum_of_changes_in_invested_money


def calculate_average_change_for_given_companies_in_particular_period(companies_tickers, start_date, end_date, set_name = None, debug_mode = False):
    sum_of_changes = 0.0
    amount_of_companies = len(companies_tickers)
    if (debug_mode):
        print("")

    for company in companies_tickers:
        print_company_name(company, debug_mode)

        share_prices_table = try_to_fetch_prices_in_particular_period(company, start_date, end_date, True, debug_mode)

        first_day_price = share_prices_table[0][0]
        last_day_price = share_prices_table[0][-1]

        print_first_and_last_day_prices(first_day_price, last_day_price, debug_mode)

        change_in_price = calculate_change_in_share_price(first_day_price, last_day_price, debug_mode)
        sum_of_changes += change_in_price

        if debug_mode:
            print("")

    average_change = sum_of_changes / amount_of_companies
    print_average_change_of_given_companies_in_given_period(average_change)
    return average_change


def calculate_change_in_share_price(first_day_price, last_day_price, debug_mode):
    change_in_price = (last_day_price - first_day_price)/first_day_price
    print_change_in_price(change_in_price, debug_mode)
    return change_in_price


def calculate_change_in_invested_money(change_in_price, company_bet_weight, debug_mode):
    change_in_invested_money = change_in_price * company_bet_weight
    print_change_in_invested_money(change_in_invested_money, debug_mode)
    return change_in_invested_money
