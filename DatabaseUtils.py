import sqlite3 as sl
from DateUtils import increaseDateByDay
from Constants import DATE_FORMAT
from PrintingUtils import printErrorSavingIntoDatabase


SQL_QUERY_CREATE_TABLE_INCOME_STATEMENTS = """CREATE TABLE IF NOT EXISTS INCOME_STATEMENT (ticker TEXT, currency TEXT, fillingDate DATE, eps FLOAT, epsDiluted FLOAT, PRIMARY KEY (ticker, fillingDate));"""
SQL_QUERY_CREATE_TABLE_SHARE_PRICES = """CREATE TABLE IF NOT EXISTS SHARE_PRICES (ticker TEXT, date DATE, currency TEXT, price FLOAT, PRIMARY KEY (ticker, date));"""
SQL_QUERY_SAVE_INCOME_STATEMENTS = 'INSERT INTO INCOME_STATEMENT (ticker, currency, fillingDate, eps, epsDiluted) values(?, ?, ?, ?, ?)'
SQL_QUERY_SAVE_SHARE_PRICES = 'INSERT INTO SHARE_PRICES (ticker, date, currency, price) values(?, ?, ?, ?)'
SQL_QUERY_READ_ALL_INCOME_STATEMENTS = 'SELECT * FROM INCOME_STATEMENT'
SQL_QUERY_READ_ALL_SHARE_PRICES = 'SELECT * FROM SHARE_PRICES'


def initializeDatabase():
    con = sl.connect('database.db')
    with con:
        con.execute(SQL_QUERY_CREATE_TABLE_INCOME_STATEMENTS)
        con.execute(SQL_QUERY_CREATE_TABLE_SHARE_PRICES)


def saveFetchedDataIntoDatabase_incomeStatements(data, debugMode = False):
    for incomeStatement in data:
        ticker = incomeStatement['symbol']
        currency = incomeStatement['reportedCurrency']
        fillingDate = incomeStatement['fillingDate']
        eps = incomeStatement['eps']
        epsDiluted = incomeStatement['epsdiluted']

        sql = SQL_QUERY_SAVE_INCOME_STATEMENTS
        data = (ticker, currency, fillingDate, eps, epsDiluted)
        saveFetchedDataIntoDatabase(sql, data, debugMode)


def saveFetchedDataIntoDatabase_sharePrices(data, dateFormat, debugMode = False):
    for index, row in data.iterrows():
        date = index.strftime(dateFormat)
        ticker = row["Ticker"]
        highPrice = row["High"]
        lowPrice = row["Low"]
        averagedPrice = (highPrice + lowPrice) / 2
        # Always USD in case of share prices fetched from Yahoo through Data Reader
        currency = "USD"

        sql = SQL_QUERY_SAVE_SHARE_PRICES
        data = (ticker, date, currency, averagedPrice)
        saveFetchedDataIntoDatabase(sql, data, debugMode)


def saveFetchedDataIntoDatabase(sqlQuery, data, debugMode = False):
    con = sl.connect('database.db')
    with con:
        try:
            con.execute(sqlQuery, data)
        except:
            printErrorSavingIntoDatabase(sqlQuery, data, debugMode)


def readAllDataFromDatabase():
    con = sl.connect('database.db')
    with con:
        data = con.execute(SQL_QUERY_READ_ALL_INCOME_STATEMENTS)
        print("DATABASE TEST: INCOME_STATEMENT")
        for row in data:
            print(row)
        data = con.execute(SQL_QUERY_READ_ALL_SHARE_PRICES)
        print("DATABASE TEST: SHARE_PRICES")
        for row in data:
            print(row)


def getMostRecentIncomeStatementForGivenCompanyForGivenDate_nPeriods(numberOfPeriods, companyTicker, date, debugMode = False):
    mostRecentIncomeStatementsForThisDate = []
    con = sl.connect('database.db')
    with con:
        data = con.execute("SELECT * FROM INCOME_STATEMENT WHERE ticker = '" + companyTicker + "'" + " AND fillingDate <= '" + date + "' ORDER BY fillingDate DESC LIMIT 4")
        mostRecentIncomeStatementForThisDate = data.fetchall()
        # if (debugMode):
        #     print("DEBUG LOG: " + "MOST RECENT INCOME STATEMENT " + companyTicker)
        #     print(mostRecentIncomeStatementForThisDate)
    return mostRecentIncomeStatementForThisDate


def getMostRecentIncomeStatementForGivenCompanyForGivenDate(companyTicker, date, debugMode = False):
    mostRecentIncomeStatementForThisDate = None
    con = sl.connect('database.db')
    with con:
        data = con.execute("SELECT * FROM INCOME_STATEMENT WHERE ticker = '" + companyTicker + "'" + " AND fillingDate <= '" + date + "' ORDER BY fillingDate DESC LIMIT 1")
        mostRecentIncomeStatementForThisDate = data.fetchone()
        # if (debugMode):
        #     print("DEBUG LOG: " + "MOST RECENT INCOME STATEMENT " + companyTicker)
        #     print(mostRecentIncomeStatementForThisDate)
    return mostRecentIncomeStatementForThisDate


def readSharePricesPerParticularPeriod(company, startDate, endDate):
    con = sl.connect('database.db')
    data = []
    with con:
        data = con.execute("SELECT * FROM SHARE_PRICES WHERE ticker = '" + company + "' AND date >='" + startDate + "' AND date <='" + endDate +"'")
    valuesToExport = []
    for row in data.fetchall():
        valuesToExport.append((row[1], row[3]))
    return valuesToExport


def tryToFetchPricesInParticularPeriod(company, startDate, endDate, isItLastSubPeriod, debugMode):
    sharePricesTable = readSharePricesPerParticularPeriod(company, startDate, endDate)
    if isItLastSubPeriod == False:
        endDate_variable = endDate
        # I want to try to increase 4 times, on 5th attempt - print error. The loop works in 0 - (n-1) range.
        AMOUNT_OF_DATE_INCREASE_TRIES = 4
        for i in range(0, (AMOUNT_OF_DATE_INCREASE_TRIES + 1)):
            lastDate = sharePricesTable[-1][0]
            if (lastDate >=endDate):
                break
            else:
                if (i < AMOUNT_OF_DATE_INCREASE_TRIES):
                    endDate_variable = increaseDateByDay(endDate_variable, DATE_FORMAT, debugMode)
                    sharePricesTable = readSharePricesPerParticularPeriod(company, startDate, endDate_variable)
                else:
                    sharePricesTable = None
                    print("ERROR: End date increased 4 times and still couldn't be read.")

    valuesToExport = [[]]
    for row in sharePricesTable:
        valuesToExport[0].append(row[1])
    return valuesToExport


def readDbSharePriceInParticularDay(company, date, debugMode):
    fetchedSharePriceData = tryToFetchPricesInParticularPeriod(company, date, date, True, debugMode)
    if (len(fetchedSharePriceData[0]) == 0):
        return None
    else:
        return fetchedSharePriceData[0][0]
