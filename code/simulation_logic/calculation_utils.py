import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from database_utils import try_to_fetch_prices_in_particular_period
from printing_utils import print_average_change_of_given_companies_in_given_period

def calculate_change_for_bets_made_for_given_companies_in_particular_period(companies_tickers_with_weights, is_it_last_sub_period, start_date, end_date):
    sum_of_changes_in_invested_money = 0.0
    for company_with_weight in companies_tickers_with_weights:
        company_ticker, company_bet_weight = company_with_weight
        share_prices_table = try_to_fetch_prices_in_particular_period(company_ticker, start_date, end_date, is_it_last_sub_period)
        first_day_price = share_prices_table[0][0]
        last_day_price = share_prices_table[0][-1]
        change_in_price = calculate_change_in_share_price(first_day_price, last_day_price)
        change_in_invested_money = calculate_change_in_invested_money(change_in_price, company_bet_weight)
        sum_of_changes_in_invested_money += change_in_invested_money
    return sum_of_changes_in_invested_money

def calculate_average_change_for_given_companies_in_particular_period(companies_tickers, start_date, end_date):
    sum_of_changes = 0.0
    amount_of_companies = len(companies_tickers)
    for company in companies_tickers:
        share_prices_table = try_to_fetch_prices_in_particular_period(company, start_date, end_date, True)
        first_day_price = share_prices_table[0][0]
        last_day_price = share_prices_table[0][-1]
        sum_of_changes += calculate_change_in_share_price(first_day_price, last_day_price)
    average_change = sum_of_changes / amount_of_companies
    print_average_change_of_given_companies_in_given_period(average_change)
    return average_change

def calculate_change_in_share_price(first_day_price, last_day_price):
    return (last_day_price - first_day_price)/first_day_price

def calculate_change_in_invested_money(change_in_price, company_bet_weight):
    return change_in_price * company_bet_weight
