# This will be the Golden Optimizer to give us beutiful lineups 
from datetime import date
import mysql.connector
from local_pydfs_lineup_optimizer import *
import constants

'''
Pulls in our projections and the sallarys of current players and optimizing for the night

Optimizes using pydfs_lineup_optimizer
'''

def getDate(day, month, year, cursor):
    findGame = 'SELECT iddates FROM dates WHERE date = %s'
    findGameData = (date(year, month, day),)
    cursor.execute(findGame, findGameData)

    dateID = -1
    for datez in cursor:
        dateID = datez[0]

    return dateID

def optimize(day, month, year, cursor):

    gameID = getDate(day, month, year, cursor)

    # get players
    playas = []
    dkPointsDict = {}
    dkPlayersPoints = {}

    getPlayersQuery = "SELECT b.nickName, p.playerID, p.fanduelPosition, p.simmonsProj, p.team, p.fanduel, p.opponent, p.fanduelPts FROM performance as p LEFT JOIN player_reference as b ON b.playerID = p.playerID WHERE p.dateID = %s AND p.projMinutes >= 8 AND p.fanduel > 0 AND p.simmonsProj IS NOT NULL AND p.simmonsProj > 0"
    getBPlayersData = (gameID,)
    cursor.execute(getPlayersQuery, getBPlayersData)

    print ("Number of players being considered: " + str(cursor.rowcount))
    players = cursor.fetchall()

    for baller in players:
        positions = []
        positions.append(str(baller[2]))
        dkPointsDict[baller[1]] = float(baller[7])
        dkPlayersPoints[baller[1]] = baller[0]

        print baller[1], baller[0], "", positions, baller[4], baller[5], baller[3]

        newPlaya = Player(baller[1], baller[0], "", positions, baller[4], int(baller[5]), float(baller[3]))
        playas.append(newPlaya)

    #instantiate optimizer + run

    optimizer = get_optimizer(Site.FANDUEL, Sport.WNBA)
    optimizer.load_players(playas)

    # if duplicate player, increase n + generate next lineup,
    # next lineup will generate lineup with next highest amount of points
    numLineups = 5

    lineups = optimizer.optimize(n=numLineups)

    for lineup in lineups:
        print(lineup)
        print(lineup.fantasy_points_projection)
        print(lineup.salary_costs)
        playerIDList = []
        dkpoints = 0
        for player in lineup.lineup:
            playerIDList.append(player.id)

        for player in playerIDList:
            dkpoints = dkpoints + dkPointsDict[player]
            playerName = dkPlayersPoints[player]

            # print optimized lineups
            print("Player Name: " + str(playerName) + "; Actual Points Scored: " + str(dkPointsDict[player]))

        print("Total Points: " + str(dkpoints))
        print ("\n")


def auto(day, month, year):


    optimize(day, month, year, cursor)

    cursor.close()
    cnx.commit()
    cnx.close()

if __name__ == "__main__":

    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()
  

    optimize(12, 6, 2018, cursor)

    cursor.close()
    cnx.commit()
    cnx.close()
