import cProfile
import pstats
import numpy as np
from config import COMPANIES_SET, START_DATE, END_DATE
from scipy.optimize import minimize

def run_profiler(command):
    # Prints the top 10 time-consuming functions
    cProfile.run(command, 'profile_stats')
    p = pstats.Stats('profile_stats')
    p.sort_stats('time').print_stats(10)

# Finding parameters doesn't work well enough.
def objective_function(x, *args):
    companies_set, start_date, end_date, tested_function = args[:4]
    optimized_params = x.tolist()
    print("Optimized Parameters:", optimized_params)
    result = tested_function(companies_set, start_date, end_date, *optimized_params)
    print("Objective Function Result:", result)
    return -result

def find_optimal_parameters(tested_function, arg1_values, arg2_values):
    initial_guess = [arg1_values[0], arg2_values[0]]
    print("Initial Guess:", initial_guess)
    # Use minimize function for optimization
    result = minimize(objective_function, initial_guess, method='Powell',
                    bounds=[(min(arg1_values), max(arg1_values)), (min(arg2_values), max(arg2_values))],
                    args=(COMPANIES_SET, START_DATE, END_DATE, tested_function))

    best_period_length_in_days, best_number_of_reports_for_calculation = result.x
    best_result = -result.fun  # Convert back to the maximization problem
    print("Best period_length_in_days:", best_period_length_in_days)
    print("Best number_of_reports_for_calculation:", best_number_of_reports_for_calculation)
    print("Best Result:", best_result)

start_time = None
def _measureTime(command):
    global start_time
    if (command == "START"): start_time = time.time()
    if (command == "STOP"):
        execution_time = time.time() - start_time
        print("Execution time:", execution_time, "seconds")