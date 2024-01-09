import datetime

def split_whole_period_into_chunks(start_date, end_date, sub_period_in_days, date_format):
    sub_period_dates = []
    full_period_start_datetime = datetime.datetime.strptime(start_date, date_format)
    full_period_end_datetime = datetime.datetime.strptime(end_date, date_format)
    sub_period_start_datetime = full_period_start_datetime
    sub_period_end_datetime = full_period_start_datetime + datetime.timedelta(days=sub_period_in_days)

    while sub_period_start_datetime < full_period_end_datetime:
        # Last iteration case
        if sub_period_end_datetime > full_period_end_datetime:
            sub_period_end_datetime = full_period_end_datetime

        sub_period_start_date = sub_period_start_datetime.strftime(date_format)
        sub_period_end_date = sub_period_end_datetime.strftime(date_format)
        sub_period_dates.append((sub_period_start_date, sub_period_end_date))
        sub_period_start_datetime = sub_period_start_datetime + datetime.timedelta(days=sub_period_in_days)
        sub_period_end_datetime = sub_period_end_datetime + datetime.timedelta(days=sub_period_in_days)
    return sub_period_dates

def increase_date_by_day(date, date_format):
    date_formatted = datetime.datetime.strptime(date, date_format)
    date_formatted_increased = date_formatted + datetime.timedelta(days=1)
    return date_formatted_increased.strftime(date_format)
