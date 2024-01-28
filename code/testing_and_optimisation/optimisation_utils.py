import cProfile
import pstats

def run_profiler(command):
    # Prints the top 10 time-consuming functions
    cProfile.run(command, 'profile_stats')
    p = pstats.Stats('profile_stats')
    p.sort_stats('time').print_stats(10)
