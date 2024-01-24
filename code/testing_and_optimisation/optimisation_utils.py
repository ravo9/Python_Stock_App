import cProfile
import pstats

def run_profiler(command):
    cProfile.run(command, 'profile_stats')
    p = pstats.Stats('profile_stats')
    # Print the top 10 time-consuming functions
    p.sort_stats('time').print_stats(10)
