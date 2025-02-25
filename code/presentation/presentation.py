def display_progress(acc, total_length, money): print(f"{((acc/total_length) * 100):.2f}%" + " " + str(money), end='\r')

def present_simulation_results(money_invested_equally, money_invested_according_to_strategy, period_length_in_days, number_of_reports_for_calculation):
    print("SIMULATION: PERIOD: " + str(period_length_in_days) + " DAYS; REPORTS NUMBER: " + str(number_of_reports_for_calculation))
    print("MONEY INVESTED IN GIVEN COMPANIES EQUALLY (AVERAGE): " + "{0:.2%}".format(money_invested_equally))
    print("MONEY INVESTED IN GIVEN COMPANIES USING TESTED STRATEGY: " + "{0:.2%}".format(money_invested_according_to_strategy))