import datetime


def splitWholePeriodIntoChunks(startDate, endDate, subPeriodLengthInDays, dateFormat, debugMode):
    subPeriodDates = []

    startDate_dateTime_wholePeriod = datetime.datetime.strptime(startDate, dateFormat)
    endDate_dateTime_wholePeriod = datetime.datetime.strptime(endDate, dateFormat)

    startDate_dateTime_subPeriod = startDate_dateTime_wholePeriod
    endDate_dateTime_subPeriod = startDate_dateTime_wholePeriod + datetime.timedelta(days=subPeriodLengthInDays)

    while startDate_dateTime_subPeriod < endDate_dateTime_wholePeriod:

        # Last iteration case
        if (endDate_dateTime_subPeriod > endDate_dateTime_wholePeriod):
            endDate_dateTime_subPeriod = endDate_dateTime_wholePeriod

        startDateWithoutTime = startDate_dateTime_subPeriod.strftime(dateFormat)
        endDateWithoutTime = endDate_dateTime_subPeriod.strftime(dateFormat)

        subPeriodDates.append((startDateWithoutTime, endDateWithoutTime))

        startDate_dateTime_subPeriod = startDate_dateTime_subPeriod + datetime.timedelta(days=subPeriodLengthInDays)
        endDate_dateTime_subPeriod = endDate_dateTime_subPeriod + datetime.timedelta(days=subPeriodLengthInDays)

    if (debugMode):
        print("")
        for period in subPeriodDates:
            print("DEBUG LOG: " + "SUB-PERIOD DATES " + period[0] + " - " + period[1])
        print("")

    return subPeriodDates


def increaseDateByDay(date, dateFormat, debugMode):
    if (debugMode):
        print("DEBUG LOG: " + "DATE TO BE INCREASED " + date)
    date_formatted = datetime.datetime.strptime(date, dateFormat)
    date_formatted_increased = date_formatted + datetime.timedelta(days=1)
    date = date_formatted_increased.strftime(dateFormat)
    if (debugMode):
        print("DEBUG LOG: " + "DATE INCREASED " + date)
    return date
