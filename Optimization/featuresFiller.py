# this is current magic to aggregate data into the features table
import mysql.connector
import datetime as dt
import constants
import warnings

'''
Pull in all features and insert into the features 
'''

# goal is to populate the database with all the features

def getDate(day, month, year, cursor):
    gameIDP = 0

    findGame = "SELECT iddates FROM dates WHERE date = %s"
    findGameData = (dt.date(year, month, day),)
    cursor.execute(findGame, findGameData)

    for game in cursor:
        gameIDP = game[0]

    return gameIDP


def getDates(day, month, year, numdays, cursor):
    base = dt.date(year, month, day)
    dateList = [base - dt.timedelta(days=x) for x in range(0, numdays)]

    listOfBadDateIDs = [711,741,796,797,798,799,800,801,920,932,951,1005,1006,1007,1008,1009,1010]
    # get date ids from database
    gameIDs = []
    for date in dateList:
        findGame = "SELECT iddates FROM dates WHERE date = %s"
        findGameData = (date,)
        cursor.execute(findGame, findGameData)

        for game in cursor:
            if game[0] not in listOfBadDateIDs:
                gameIDs.append(game[0])

    return gameIDs
def fill(year, month, day, numdays, cursor):
    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

    dateIDs = getDates(day, month, year, numdays, cursor)

    # example of what this is doing
    # week 2 lonzo ball data - feature, target - score
    # ..........
    # .......
    # week 4 day - lonzo ball's data - feature, target - ?

    # TODO: train only on players that aren't playing in garbage time
    # TODO: [932 , 1022)

    numpyDataArrays = []

    # add minutes constraint
    get_players = "Select playerID from performance where dateID = %s"
    getDailyPlayerAvg = "SELECT blocks, points, steals, AST, turnovers, totalRebounds, tripleDouble, doubleDouble, 3PM, oRebound, dRebound, minutes, FG, FGA, FGP, 3PA, 3PP, FTM, FTA, FTP, personalFouls, plusMinus, trueShootingP, eFG, freeThrowAttemptRate, 3PointAttemptRate, oReboundP, dReboundP, totalReboundP, ASTP, STP, BLKP, turnoverP, USG, oRating, dRating FROM player_daily_avg WHERE dateID = %s AND playerID = %s"
    getPerformanceDataForEachPlayer = "SELECT playerID, dateID, fanduel, draftkings, fanduelPosition, draftkingsPosition, team, opponent, fanduelPts, draftkingsPts, projMinutes FROM performance WHERE dateID = %s and projMinutes IS NOT NULL AND fanduelPosition IS NOT NULL"
    get_guards = "Select blocks, points, steals, assists, turnovers, tRebounds, DDD, DD, 3PM, 3PA, oRebounds, dRebounds, minutes, FG, FGA, FT, FTA, BPM, PPM, SPM, APM, TPM, DDDPG, DDPG, 3PP, ORPM, DRPM, FGP, FTP, usg, ORT, DRT, TS, eFG from team_vs_guards WHERE dateID = %s and dailyTeamID = %s"
    get_fowards = "Select blocks, points, steals, assists, turnovers, tRebounds, DDD, DD, 3PM, 3PA, oRebounds, dRebounds, minutes, FG, FGA, FT, FTA, BPM, PPM, SPM, APM, TPM, DDDPG, DDPG, 3PP, ORPM, DRPM, FGP, FTP, usg, ORT, DRT, TS, eFG from team_vs_fowards WHERE dateID = %s and dailyTeamID = %s"

    getTeamData = "SELECT avgPointsAllowed, avgPointsScored FROM team_daily_avg_performance WHERE dateID = %s AND dailyTeamID = %s"

    insert_features = "Insert into features (idfeatures, playerID, dateID, projMinutes, fanduel, draftkings, blocksDPA, pointsDPA, stealsDPA, AST_DPA, turnoversDPA, totalReboundsDPA, tripleDoubleDPA, doubleDoubleDPA, 3PM_DPA, oReboundDPA, dReboundDPA, minutesDPA, FG_DPA, FGA_DPA, FGP_DPA, 3PA_DPA, 3PP_DPA, FTM_DPA, FTA_DPA, FTP_DPA, personalFoulsDPA, plusMinusDPA, trueShootingP_DPA, eFG_DPA, freeThrowAttemptRateDPA, 3PointAttemptRateDPA, oReboundP_DPA, dReboundP_DPA, totalReboundP_DPA, ASTP_DPA, STP_DPA, BLKP_DPA, turnoverP_DPA, USG_DPA, oRatingDPA, dRatingDPA, blocksTvP, pointsTvP, stealsTvP, assistsTvP, turnoversTvP, tReboundsTvP, dddTvP, ddTvP, 3pmTvP, 3paTvP, oReboundsTvP, dReboundsTvP, minutesTvP, fgTvP, fgaTvP, ftTvP, ftaTvP, bpmTvP, ppmTvP, spmTvP, apmTvP, tpmTvP, dddpgTvP, ddpgTvP, 3ppTvP, orpmTvP, drpmTvP, fgpTvP, ftpTvP, usgTvP, ortTvP, drtTvP, tsTvP, efgTvP, avgPointsAllowedTeam, avgPointsScoredTeam) values (%s, %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s,  %s, %s)" 
    # execute command + load into numpy array
    playersPlaying = []
    for date in dateIDs:
        print date
        dateD = (date,)
        cursor.execute(getPerformanceDataForEachPlayer, dateD)
        results = cursor.fetchall()
        print getPerformanceDataForEachPlayer
        for player in results:
            playersPlaying.append(player)

    # get daily_player_avg
    # get opp_team stats
    # get self_team stats
    # get opp_vs_player position states
    # from perfromance get fanduel point for taraget
    team_ref_query = "SELECT teamID FROM team_reference WHERE bbreff = %s"

    counter = 0

    allPlayerFeatures = []
    playersActuallyPlaying = []
    features = ()
    print(len(playersPlaying))
    getLastID = "Select MAX(idfeatures) from features"
    cursor.execute(getLastID)
    try:
        feaID = int(cursor.fetchall()[0][0])
    except:
        feaID = 0
    feaID += 1
    for player in playersPlaying:

        checkPlayerDailyAvgData = (player[1], player[0])
        cursor.execute(getDailyPlayerAvg, checkPlayerDailyAvgData)

        # check to see + skip to next player if not in set
        check = cursor.fetchall()
        if len(check) == 0:
            continue

        # player and date id for reference
        features = features + (feaID,)
        features = features + (player[0], player[1])

        # fanduel + dk salaries to features
        features = features + (player[2], 0)

        indvPlayerData = []
        
	indvPlayerData.append(feaID)
	indvPlayerData.append(player[0])
	indvPlayerData.append(player[1])
        indvPlayerData.append(player[10])
	indvPlayerData.append(player[2])
	indvPlayerData.append(0)
        basicQueryData = (player[1], player[0])
        cursor.execute(getDailyPlayerAvg, basicQueryData)

        playerDailyAvgResult = cursor.fetchall()

        # append playerDailyAvgResult to indvPlayerData
        for item in playerDailyAvgResult[0]:
            features = features + (item,)
            indvPlayerData.append(item)

       # teamID from player and use team reference table to get playerID
        teamIDData = (player[6],)
        cursor.execute(team_ref_query, teamIDData)
        oppTeamID = cursor.fetchall()

        oppTeamIDData = (player[7],)
        cursor.execute(team_ref_query, teamIDData)
        teamID = cursor.fetchall()

        # use teamID + date ID to query the team data and opp team data for that date
        # append to master array
        idTeam = 0
        for team in teamID:
            idTeam = team[0]

        idOppTeam = 0
        for oppTeam in oppTeamID:
            idOppTeam = oppTeam[0]

        teamQuery = (player[1], idTeam)
        cursor.execute(getTeamData, teamQuery)
        teamResult = cursor.fetchall()

        oppTeamQuery = (player[1], idOppTeam)
        cursor.execute(getTeamData, oppTeamQuery)
        oppTeamResult = cursor.fetchall()

        # use position + dateID + opp team ID to query team vs. defense for that position
        # append to master array
        # doubl'n it!
        if player[4] == 'G':
            pos_data = (player[1], idOppTeam)
            cursor.execute(get_guards, pos_data)
            ball_handlers_results = cursor.fetchall()

            for item in ball_handlers_results[0]:
                features = features + (item,)
                indvPlayerData.append(item)
        
        if player[4] == 'F':
            pos_data = (player[1], idOppTeam)
            cursor.execute(get_fowards, pos_data)
            ball_handlers_results = cursor.fetchall()
	  

            for item in ball_handlers_results[0]:
                features = features + (item,)
                indvPlayerData.append(item)
 
        for item in teamResult[0]:
            indvPlayerData.append(item)
               
        
	features = tuple(indvPlayerData)
        cursor.execute(insert_features, features)
        feaID += 1
        features = ()
        playersActuallyPlaying.append(player)

    selectQuery = "SELECT playerID, dateID FROM features WHERE fanduelPts IS NULL"
    selectPerformance = "SELECT fanduelPts, draftkingsPts FROM performance WHERE playerID = %s AND dateID = %s"

    insertFeature = "UPDATE features SET fanduelPts = %s, draftkingsPts = %s WHERE playerID = %s AND dateID = %s"

    cursor.execute(selectQuery)

    playersPlayed = cursor.fetchall()

    for player in playersPlayed:
        pData = (player[0], player[1])
        cursor.execute(selectPerformance, pData)

        insertData = cursor.fetchall()

        insertDataT = (insertData[0][0], insertData[0][1], player[0], player[1])

        cursor.execute(insertFeature, insertDataT)

if __name__ == "__main__":
    print("Loading data...")
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()
  
    # dates to retrieve data for batter test data
    year = constants.gdStartYear
    month = constants.gdStartMonth
    day = constants.gdStartDay

    numdays = constants.numdaysGradientDescent

    fill(year, month, day, numdays, cursor)
    cnx.commit()
    cursor.close()

  
