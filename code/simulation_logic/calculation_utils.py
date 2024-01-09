import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from database_utils import try_to_fetch_prices_in_particular_period

calculate_change_in_share_price = lambda first_day_price, last_day_price: (last_day_price - first_day_price)/first_day_price

calculate_change_in_invested_money = lambda change_in_price, company_bet_weight: change_in_price * company_bet_weight

def calculate_change_for_bets_made_for_given_companies_in_given_period(companies_tickers_with_weights, is_it_last_sub_period, start_date, end_date):
    sum_of_changes_in_invested_money = 0.0
    for company_with_weight in companies_tickers_with_weights:
        company_ticker, company_bet_weight = company_with_weight
        share_prices_table = try_to_fetch_prices_in_particular_period(company_ticker, start_date, end_date, is_it_last_sub_period)
        first_day_price = share_prices_table[0][0]
        last_day_price = share_prices_table[0][-1]
        change_in_price = calculate_change_in_share_price(first_day_price, last_day_price)
        sum_of_changes_in_invested_money += calculate_change_in_invested_money(change_in_price, company_bet_weight)
    return sum_of_changes_in_invested_money

def calculate_average_share_price_change_for_given_companies_in_given_period(companies_tickers, start_date, end_date):
    sum_of_changes = 0.0
    for company in companies_tickers:
        share_prices_table = try_to_fetch_prices_in_particular_period(company, start_date, end_date, True)
        first_day_price = share_prices_table[0][0]
        last_day_price = share_prices_table[0][-1]
        sum_of_changes += calculate_change_in_share_price(first_day_price, last_day_price)
    return sum_of_changes / len(companies_tickers)
