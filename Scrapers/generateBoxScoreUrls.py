# will generate basektball reference box score urls for scraping
import mysql.connector
from datetime import timedelta, date
import constants
import urllib2
team_abrev = ["ATL", "CHI", "CON", "IND", "LAS", "MIN", "NYL", "PHO", "LVA", "SEA", "DAL", "WAS"] 

def findDate(year, month, day, cursor):
    findGame = 'SELECT iddates FROM dates WHERE date = %s'
    findGameData = (date(year, month, day),)
    cursor.execute(findGame, findGameData)

    dateID = -1
    for datez in cursor:
        dateID = datez[0]

    return dateID

# function to iterate through a range of dates in the scrapers
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def generateDates(startDay, startMonth, startYear, endDay, endMonth, endYear):
    start_date = date(startYear, startMonth, startDay)
    end_date = date(endYear, endMonth, endDay)
    dates = []
    for single_date in daterange(start_date, end_date):
        dates.append(single_date)
    return dates

# function that generates all valid basketball reference urls
def generateUrls(cursor,cnx, dates):
    urls = []
    badURLs = []
    baseURL = "https://www.basketball-reference.com/wnba/boxscores/" 

    for date in dates:
        print date
        for team in team_abrev:
            shouldSave = len(urls) % 1
            if shouldSave == 0 and len(urls) != 0:
                queryBoxScoreURL = "INSERT INTO box_score_urls (url, dateID) VALUES (%s, %s)"
                cursor.execute(queryBoxScoreURL, urls[0])
                cnx.commit()
                print "Inserted + Committed URLs"
                urls = []

            month = ""
            day = ""

            if len(str(date.month)) == 1:
                month = "0" + str(date.month)
            else:
                month = str(date.month)

            if len(str(date.day)) == 1:
                day = "0" + str(date.day)
            else:
                day = str(date.day)

            newURL = baseURL + str(date.year) + month + day + str(0) + team + ".html"
            try:
                urllib2.urlopen(newURL)
                boxScoreID = findDate(date.year, date.month, date.day, cursor)

                urlTuple = (newURL, boxScoreID)
                urls.append(urlTuple)
            except:
                badURLs.append(newURL)

def main():
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()

    dates = generateDates(constants.startDayP, constants.startMonthP, constants.startYearP,
                  constants.endDayP, constants.endMonthP, constants.endYearP)

    generateUrls(cursor, cnx, dates)

    cursor.close()

if __name__ == "__main__":
    main()
