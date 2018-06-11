# this will sum points for performance table so we know what fanduel score they got
import mysql.connector
import constants
import datetime as dt

def getDate(day, month, year, cursor):
    gameIDP = 0

    findGame = "SELECT iddates FROM new_dates WHERE date = %s"
    findGameData = (dt.date(year, month, day),)
    cursor.execute(findGame, findGameData)

    for game in cursor:
        gameIDP = game[0]

    return gameIDP

def auto(dateID, cursor):
    sum2 = "update performance set fanduelPts = (FT + totalRebounds*1.2 + assists*1.5 + blocks*3 + steals*3 - turnovers + (3PM)*3 + (fieldGoals-3PM)*2) where dateID = %s"

    joinFDDKPoints = "UPDATE features as f INNER JOIN performance as p ON (f.dateID = p.dateID AND f.playerID = p.playerID) SET f.draftkingsPts = p.draftkingsPts, f.fanduelPts = p.fanduelPts WHERE p.dateID = %s AND f.dateID = %s"

    dateToJoin = dateID

    joinData = (dateToJoin,)
    joinJoinData = (dateToJoin, dateToJoin)
    cursor.execute(sum2, joinData)
    print "Updated FanDuel Points"
    cnx.commit()
    cursor.execute(joinFDDKPoints, joinJoinData)
    print "Updated Futures DK and FD Points"

    cursor.close()
    cnx.commit()
    cnx.close()
    


if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()
    
    auto(constants.todayID, cursor)

    cursor.close()
    cnx.commit()
    cnx.close()
