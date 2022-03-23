from pathlib import Path
import os


def check_if_txt_log_exists(output_dir):
    log_file_path = Path(output_dir + 'log.txt')
    if log_file_path.is_file() == False:
        os.system("mkdir " + output_dir)
        os.system("touch " + str(log_file_path))


def write_result_into_txt_log_set_name(output_dir, set_name = ""):
    check_if_txt_log_exists(output_dir)
    with open((output_dir + 'log.txt'),'a') as f:
        f.write("\n")
        f.write(set_name + "\n")


def write_result_into_txt_log_periods(output_dir, whole_period_length, sub_period_length):
    check_if_txt_log_exists(output_dir)
    with open((output_dir + 'log.txt'),'a') as f:
        if (whole_period_length != None):
            f.write("WHOLE PERIOD LENGTH: " + whole_period_length + "\n")
        f.write("SUB-PERIOD LENGTH: " + str(sub_period_length) + "\n")


def write_result_into_txt_log_results(output_dir, result, average_change):
    check_if_txt_log_exists(output_dir)
    with open((output_dir + 'log.txt'),'a') as f:
        f.write("MONEY AFTER ALL CHANGES ACCORDING TO MY STRATEGY IN PERCENTAGE: " + "{0:.2%}".format(result) + "\n")
        f.write("AVERAGE CHANGE OF GIVEN COMPANIES IN GIVEN PERIOD " + "{0:.2%}".format(average_change))
        f.write("\n\n")
