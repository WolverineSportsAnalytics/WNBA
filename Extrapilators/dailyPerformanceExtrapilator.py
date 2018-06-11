# This will be daily extrapilator to average out performances for the season and put into dailyPlayerAverage table
import mysql.connector
import constants

def averaging(cursor, performanceData, averageStatement, insertAvgStatement, tableID, player, date):
    cursor.execute(averageStatement, performanceData)
    
    new_cumlative = []
    cumulativeP = cursor.fetchall()
    new_cumlative.append(tableID)
    new_cumlative.append(player)
    new_cumlative.append(date)
    for item in cumulativeP[0]:
        new_cumlative.append(item)

    if new_cumlative[4] is None:
        return
    else:
        cursor.execute(insertAvgStatement, new_cumlative)

def player_total_avg(cursor, dates, players, cnx):
    # now loop, average, and insert
    average = 'select avg(blocks), avg(points), avg(steals), avg(assists), avg(turnovers), avg(totalRebounds), avg(tripleDouble), avg(doubleDouble), avg(3PM), avg(offensiveRebounds), avg(defensiveRebounds), avg(minutesPlayed), avg(fieldGoals), avg(fieldGoalsAttempted), avg(fieldGoalPercent), avg(3PA), avg(3PPercent), avg(FT), avg(FTA), avg(FTPercent), avg(personalFouls), avg(plusMinus), avg(trueShootingPercent), avg(effectiveFieldGoalPercent), avg(freeThrowAttemptRate), avg(3pointAttemptRate), avg(offensiveReboundPercent), avg(defensiveReboundPercent), avg(totalReboundPercent), avg(assistPercent), avg(stealPercent), avg(blockPercent), avg(turnoverPercent), avg(usagePercent), avg(offensiveRating), avg(defensiveRating) from performance where playerID=%s and dateID>0 and dateID < %s'

    insertAvg = "INSERT INTO player_daily_avg VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    #give table id because you can't insert all without it
    getLastID = "Select MAX(iddailyplayer) from player_daily_avg"
    cursor.execute(getLastID)
    try:
        tableID = int(cursor.fetchall()[0][0]) + 1
    except:
        tableID = 1


    for date in dates:
        print date
        for player in players:
            performanceData = (player, date)

            averaging(cursor, performanceData, average, insertAvg, tableID, player, date)

            cnx.commit()

            tableID = tableID + 1

def extrapolate(dateCutOff, upperBoundCutOff, cursor, cnx):
    getPlayerIDs = "SELECT playerID FROM player_reference"
    cursor.execute(getPlayerIDs)

    players = []
    sqlResults = cursor.fetchall()
    for row in sqlResults:
        players.append(row[0])


    getDates = "SELECT iddates FROM dates WHERE iddates >= %s AND iddates <= %s"
    getDatesD = (dateCutOff, upperBoundCutOff)
    cursor.execute(getDates, getDatesD)

    dates = []
    sqlResults = cursor.fetchall()
    for row in sqlResults:
        dates.append(row[0])

    player_total_avg(cursor, dates, players, cnx)
    

if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()
    
    dateCutOff = constants.dailyPerformanceExtrapolationDateCutOff
    upperBoundCutOff = constants.extapolatorUpperBound

    extrapolate(dateCutOff, upperBoundCutOff, cursor, cnx)

    cursor.close()
    cnx.commit()
    cnx.close()

