# will scrape box scores to get team performances
import mysql.connector
from datetime import timedelta, date
import constants
from bs4 import BeautifulSoup, Comment
import datetime as dt
import requests


# Gets the date specified in new_dates
def getDate(day, month, year, cursor):
    gameIDP = 0

    findGame = "SELECT iddates FROM dates WHERE date = %s"
    findGameData = (dt.date(year, month, day),)
    cursor.execute(findGame, findGameData)

    for game in cursor:
        gameIDP = game[0]

    return gameIDP


# find the daterange to update 
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


# update and insert stats into the team_performance table
def updateAndInsertPlayerRef(
        startDay,
        startMonth,
        startYear,
        endDay,
        endMonth,
        endYear,
        cursor,
        cnx):

    # sql statement to insert into our database
    insert_team_data = "INSERT INTO team_performance (dailyTeamID, dailyTeamOpponentID, dateID, pointsAllowed, pointsScored) Values(%s, %s, %s, %s, %s)" 

    start_date_id = getDate(startDay, startMonth, startYear, cursor)
    end_date_id = getDate(endDay, endMonth, endYear, cursor)

    select_dates = "Select * from box_score_urls WHERE dateID >= %s AND dateID <= %s"
    boxScoreDatesD = (start_date_id, end_date_id)
    cursor.execute(select_dates, boxScoreDatesD)
    box_url = cursor.fetchall()
    url = []

    start_date = date(startYear, startMonth, startDay)
    end_date = date(endYear, endMonth, endDay)

    dates = []
    for single_date in daterange(start_date, end_date):
        dates.append(str(single_date.year) + '-' +
                     str(single_date.month) + '-' + str(single_date.day))

    date_counter = 0

    # loop through all url's for all of the games
    for urls in box_url:
        url = urls[1]
        date_id = urls[2]
        print date_id
        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html.parser')
        mydivs = soup.findAll("div", {"class": "scorebox"})
        teams = []
        for i in mydivs:
            for j in i.find_all('a'):
                team = j['href'].split('/')[3]
                if len(team) == 3:
                    teams.append(team)


        scores =mydivs[0].findAll("div", {"class":"score"})
        h_score = scores[0].text
        a_score = scores[1].text
        h_team = teams[0]
        a_team = teams[1]


        selec_id = "select teamID from team_reference where bbreff=\""

        get_team = selec_id + h_team + "\""
        cursor.execute(get_team)
        h_team_id = cursor.fetchall()[0][0]

        get_team = selec_id + a_team + "\""
        cursor.execute(get_team)
        a_team_id = cursor.fetchall()[0][0]

        h_insert = (h_team_id, a_team_id, date_id, a_score, h_score)
        cursor.execute(insert_team_data, h_insert)

        a_insert = (a_team_id, h_team_id, date_id, h_score, a_score)
        cursor.execute(insert_team_data, a_insert)

        cnx.commit()
        

        



if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)               


    cursor = cnx.cursor(buffered=True)

    updateAndInsertPlayerRef(
        constants.startDayP,
        constants.startMonthP,
        constants.startYearP,
        constants.endDayP,
        constants.endMonthP,
        constants.endYearP,
        cursor,
        cnx)

    cursor.close()
    cnx.commit()
    cnx.close()
