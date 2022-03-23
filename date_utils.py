import datetime


def split_whole_period_into_chunks(start_date, end_date, sub_period_length_in_days, date_format, debug_mode):
    sub_period_dates = []

    start_date_datetime_whole_period = datetime.datetime.strptime(start_date, date_format)
    end_date_datetime_whole_period = datetime.datetime.strptime(end_date, date_format)

    start_date_datetime_sub_period = start_date_datetime_whole_period
    end_date_datetime_sub_period = start_date_datetime_whole_period + datetime.timedelta(days=sub_period_length_in_days)

    while start_date_datetime_sub_period < end_date_datetime_whole_period:

        # Last iteration case
        if end_date_datetime_sub_period > end_date_datetime_whole_period:
            end_date_datetime_sub_period = end_date_datetime_whole_period

        start_date_without_time = start_date_datetime_sub_period.strftime(date_format)
        end_date_without_time = end_date_datetime_sub_period.strftime(date_format)

        sub_period_dates.append((start_date_without_time, end_date_without_time))

        start_date_datetime_sub_period = start_date_datetime_sub_period + datetime.timedelta(days=sub_period_length_in_days)
        end_date_datetime_sub_period = end_date_datetime_sub_period + datetime.timedelta(days=sub_period_length_in_days)

    if debug_mode:
        print("")
        for period in sub_period_dates:
            print("DEBUG LOG: " + "SUB-PERIOD DATES " + period[0] + " - " + period[1])
        print("")

    return sub_period_dates


def increase_date_by_day(date, date_format, debug_mode):
    if debug_mode:
        print("DEBUG LOG: " + "DATE TO BE INCREASED " + date)
    date_formatted = datetime.datetime.strptime(date, date_format)
    date_formatted_increased = date_formatted + datetime.timedelta(days=1)
    date = date_formatted_increased.strftime(date_format)
    if debug_mode:
        print("DEBUG LOG: " + "DATE INCREASED " + date)
    return date
