# will scrape box scores for daily performance
import mysql.connector
from bs4 import BeautifulSoup, Comment
import requests
import constants
import datetime as dt
from datetime import timedelta, date

def getDate(day, month, year, cursor):
    gameIDP = 0

    findGame = "SELECT iddates FROM dates WHERE date = %s"
    findGameData = (dt.date(year, month, day),)
    cursor.execute(findGame, findGameData)

    for game in cursor:
        gameIDP = game[0]

    return gameIDP


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def generateURLs(startDay, startMonth, startYear, endDay, endMonth, endYear):
    start_date = date(startYear, startMonth, startDay)
    end_date = date(endYear, endMonth, endDay)
    urls = []
    for single_date in daterange(start_date, end_date):
        urls.append('https://www.basketball-reference.com/friv/dailyleaders.fcgi?month=' + str(
            single_date.month) + '&day=' + str(single_date.day) + '&year=' + str(single_date.year))
    return urls


def updateAndInsertPlayerRef(
        startDay,
        startMonth,
        startYear,
        endDay,
        endMonth,
        endYear,
        cursor,
        cnx):

    # set range of dates
    # urls = generateURLs(startDay, startMonth, startYear, endDay, endMonth, endYear)

    start_date_id = getDate(startDay, startMonth, startYear, cursor)
    print start_date_id
    end_date_id = getDate(endDay, endMonth, endYear, cursor)
    print end_date_id


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

    selec_id_id = "select playerID from player_reference where bbrefID= %s"
    selec_id = "select playerID from player_reference where nickName=\""

    date_counter = 0

    # loop through all url's
    for score in box_url:


        url = score[1]
        print url
        date_id = score[2]
        # print get_date
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        soup.findAll(text=lambda text: isinstance(text, Comment))
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))

        comment = comments[len(comments) - 24]
        soup1 = BeautifulSoup(comment, "html.parser")

        teams = []
        # get teams
        mydivs = soup.findAll("div", {"class": "scorebox"})
        for i in mydivs:
            for j in i.find_all('a'):
                team = j['href'].split('/')[3]
                if len(team) == 3:
                    teams.append(team)

        tables = soup.find_all("tbody")

        team_tables = [[tables[0],teams[0], teams[1], 0], [
            tables[1], teams[1], teams[0], 1]]

        for team in team_tables:
            # set team specific data
            tea = team[1]
            opp = team[2]
            basic_table = team[0].find_all('tr')
            home = team[3]
            # scrape regular stats
            for number in range(len(basic_table)):
                # first find, then updated
                    try:
                        bbrefID = basic_table[number].find_all('th')[0].find_all('a')[0]['href']
                        bbrefID = bbrefID.split('/')[4].split(".")[0]
                        bbrefData = (bbrefID,)
                        cursor.execute(selec_id_id, bbrefData)
                        player_id = cursor.fetchall()[0][0]
                    except:
                        pass

                    try:
                        nickName = basic_table[number].find_all('th')[0].a.text
                        tds1 = basic_table[number].find_all('td')
                        get_id = selec_id + nickName + "\""
                        cursor.execute(get_id)
                        player_id = cursor.fetchall()[0][0]
                    except:
                        pass


                    try:
                        if tds1[0].text == "Did Not Play":
                            inutes = 0
                            blocks = 0
                            steals = 0
                            points = 0
                            assists = 0
                            to = 0
                            rebounds = 0
                            triple_double = 0
                            double_double = 0
                            o_rebs = 0
                            d_rebs = 0
                            fgs = 0
                            fga = 0
                            fgpercent = 0
                            tpm = 0
                            tpa = 0
                            tp_percent = 0
                            free_throws = 0
                            fta = 0
                            ft_percent = 0
                            pf = 0
                        else:
                            minutes = tds1[0].text.split(":")[0]

                            blocks = tds1[11].text
                            steals = tds1[10].text
                            points = tds1[14].text
                            assists = tds1[9].text
                            to = tds1[12].text
                            rebounds = tds1[8].text
                            triple_double = 0
                            double_double = 0
                            o_rebs = tds1[7].text
                            d_rebs = rebounds = o_rebs

                            fgs = tds1[1].text
                            fga = tds1[2].text
                            if fga == 0:
                                fgpercent = "NULL"
                            else:
                                fgpercent = tds1[3].text

                            tpm = tds1[4].text
                            tpa = tds1[5].text
                            if tpa == 0:
                                tp_percent = "NULL"
                            else:
                                tp_percent = tds1[6].text

                            free_throws = tds1[7].text
                            fta = tds1[8].text
                            if fta == 0:
                                ft_percent = "NULL"
                            else:
                                ft_percent = tds1[9].text

                            pf = tds1[13].text

                            plus_minus = '0'

                            plus_tens = 0
                            if int(steals) >= 10:
                                plus_tens += 1
                            if int(blocks) >= 10:
                                plus_tens += 1
                            if int(points) >= 10:
                                plus_tens += 1
                            if int(assists) >= 10:
                                plus_tens += 1
                            if int(rebounds) >= 10:
                                plus_tens += 1

                            if plus_tens > 2:
                                triple_double = 1
                            elif plus_tens > 1:
                                double_double = 1
                        inserts = (
                            player_id,
                            date_id,
                            points,
                            minutes,
                            fgs,
                            fga,
                            fgpercent,
                            tpm,
                            tpa,
                            tp_percent,
                            free_throws,
                            fta,
                            ft_percent,
                            o_rebs,
                            d_rebs,
                            rebounds,
                            assists,
                            steals,
                            blocks,
                            to,
                            pf,
                            triple_double,
                            double_double,
                            tea,
                            opp,
                            home)
                        

                        new_insert = (
                            points,
                            minutes,
                            fgs,
                            fga,
                            fgpercent,
                            tpm,
                            tpa,
                            tp_percent,
                            free_throws,
                            fta,
                            ft_percent,
                            o_rebs,
                            d_rebs,
                            rebounds,
                            assists,
                            steals,
                            blocks,
                            to,
                            pf,
                            triple_double,
                            double_double,
                            tea,
                            opp,
                            home,
                            player_id,
                            date_id
                            )
                        update_performance = "INSERT INTO performance (playerID, dateID, points, minutesPlayed, fieldGoals, fieldGoalsAttempted, fieldGoalPercent, 3PM, 3PA, 3PPercent, FT, FTA, FTPercent, offensiveRebounds, defensiveRebounds, totalRebounds, assists,  steals, blocks, turnovers, personalFouls, tripleDouble, doubleDouble, team, opponent, home) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                        true_update_perf = "UPDATE performance set points=%s, minutesPlayed=%s, fieldGoals=%s, fieldGoalsAttempted=%s, fieldGoalPercent=%s, 3PM=%s, 3PA=%s, 3PPercent=%s, FT=%s, FTA=%s, FTPercent=%s, offensiveRebounds=%s, defensiveRebounds=%s, totalRebounds=%s, assists=%s,  steals=%s, blocks=%s, turnovers=%s, personalFouls=%s, tripleDouble=%s, doubleDouble=%s, team=%s, opponent=%s, home=%s where playerID= %s and dateID = %s"

                        check = "SELECT * from performance where dateID = %s and playerID = %s"
                        cursor.execute(check,(date_id,player_id))
                        checks = cursor.fetchall()
                        if len(checks) > 0:
                            cursor.execute(true_update_perf, new_insert)
                            cnx.commit()


                        else:
                            cursor.execute(update_performance, inserts)

                        cnx.commit()
                    except Exception,e: 
                        print str(e)


    cleanUp = "DELETE FROM performance WHERE blocks IS NULL"
    cursor.execute(cleanUp)

    cursor.close()
    cnx.commit()
    cnx.close()


if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)               

    cursor = cnx.cursor()

    updateAndInsertPlayerRef(
        constants.startDayP,
        constants.startMonthP,
        constants.startYearP,
        constants.endDayP,
        constants.endMonthP,
        constants.endYearP,
        cursor,
        cnx)


