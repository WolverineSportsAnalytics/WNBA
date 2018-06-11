# Extrapolates team vs Defense informatio:vi
import mysql.connector
import constants

blockIdx = 0
pointsIdx = 1
stealsIdx = 2
assistsIdx = 3
turnoversIdx = 4
totalRIdx = 5
tripleDoubleIdx = 6
doubleDoubleIdx = 7
threePMIdx = 8
threePAIdx = 9
offensiveReboundsIdx = 10
defensiveReboundsIdx = 11
minutesPlayedIdx = 12
fieldGoalsIdx = 13
fieldGoalsAttemptedIdx = 14
FTIdx = 15
FTAIdx = 16
usageIdx = 17
ortIdx = 18
drtIdx = 19
tStIdx = 20
eFGIdx = 21


def averaging(cursor, team, dateLower, dateUpper, tableID, playasVsOpponentsScript, teamVsGuardsScript, teamVsFowardsScript,cnx):
    # get all players who played vs that team before that day
    # separate players into the buckets aboved based on their position

    getPlayersVsOpponents = playasVsOpponentsScript
    insertTeamVsDefenseGuards = teamVsGuardsScript
    insertTeamVsDefenseFowards = teamVsFowardsScript


    # get all ball handlers
    playerVsOpponentsData = (team, dateLower, dateUpper, 'G')
    cursor.execute(getPlayersVsOpponents, playerVsOpponentsData)
    Guards = cursor.fetchall()

    playerVsOpponentsData = (team, dateLower, dateUpper, 'F')
    cursor.execute(getPlayersVsOpponents, playerVsOpponentsData)
    Fowards = cursor.fetchall()




    players = {'guards': Guards, 'fowards': Fowards}
    for key, value in players.items():
        ##############################
        # for each player in bucket
        # (sum all stats / games played till that point)
        blocks = 0
        points = 0
        steals = 0
        assists = 0
        turnovers = 0
        totalRebounds = 0
        tripleDouble = 0
        doubleDouble = 0
        threePM = 0
        threePA = 0
        offensiveRebounds = 0
        defensiveRebounds = 0
        minutesPlayed = 0
        fieldGoals = 0
        fieldGoalsAttempted = 0
        FT = 0
        FTA = 0
        usagePercent = 0
        offensiveRating = 0
        defensiveRating = 0
        trueShootingPercent = 0
        effectiveFieldGoalPercent = 0

        # unlazy but position = ballHandler
        for ballHandler in value:
            print ballHandler
            blocks = blocks + ballHandler[blockIdx]
            points = points + ballHandler[pointsIdx]
            steals = steals + ballHandler[stealsIdx]
            assists = assists + ballHandler[assistsIdx]
            turnovers = turnovers + ballHandler[turnoversIdx]
            totalRebounds = totalRebounds + ballHandler[totalRIdx]
            tripleDouble = tripleDouble + ballHandler[tripleDoubleIdx]
            doubleDouble = doubleDouble + ballHandler[doubleDoubleIdx]
            threePM = threePM + ballHandler[threePMIdx]
            threePA = threePA + ballHandler[threePAIdx]
            offensiveRebounds = offensiveRebounds + ballHandler[offensiveReboundsIdx]
            defensiveRebounds = defensiveRebounds + ballHandler[defensiveReboundsIdx]
            minutesPlayed = minutesPlayed + ballHandler[minutesPlayedIdx]
            fieldGoals = fieldGoals + ballHandler[fieldGoalsIdx]
            fieldGoalsAttempted = fieldGoalsAttempted + ballHandler[fieldGoalsAttemptedIdx]
            FT = FT + ballHandler[FTIdx]
            FTA = FTA + ballHandler[FTAIdx]
        
        blocksPerMinute = float(blocks) / minutesPlayed if minutesPlayed else 0
        pointsPerMinute = float(points) / minutesPlayed if minutesPlayed else 0
        stealsPerMinute = float(steals) / minutesPlayed if minutesPlayed else 0
        assistsPerMinute = float(assists) / minutesPlayed if minutesPlayed else 0
        turnoversPerMinute = float(turnovers) / minutesPlayed if minutesPlayed else 0
        tripleDoubles = float(tripleDouble) / len(Guards) if len(Guards) else 0
        doubleDoubles = float(doubleDouble) / len(Guards) if len(Guards) else 0
        threePP = float(threePM) / float(threePA) if threePA else 0
        offensiveReboundsPerMinute = float(offensiveRebounds) / minutesPlayed if minutesPlayed else 0
        defensiveReoundsPerMinute = float(defensiveRebounds) / minutesPlayed if minutesPlayed else 0
        fieldGoalP = float(fieldGoals) / float(fieldGoalsAttempted) if fieldGoalsAttempted else 0
        FTP = float(FT) / float(FTA) if FTA else 0
        usagePercentTot = 0
        offensiveRatingTot = 0
        defensiveRatingTot = 0
        trueShooting = points / (2 * (float(fieldGoalsAttempted) + 0.44 * FTA)) if fieldGoalsAttempted else 0
        effectiveFieldGoal = (float(fieldGoals) + 0.5 * float(threePM)) / float(
            fieldGoalsAttempted) if fieldGoalsAttempted else 0

        # get team id
        teamIDQ = "SELECT teamID FROM team_reference WHERE bbreff = %s"
        teamIDD = (team,)
        cursor.execute(teamIDQ, teamIDD)

        teamID = 0
        for id in cursor.fetchall():
            teamID = id[0]

    
        teamVsPlayerData = (tableID, teamID, dateUpper, blocks, points, steals, assists, turnovers, totalRebounds, tripleDouble, doubleDouble, threePM, threePA, offensiveRebounds, defensiveRebounds, minutesPlayed, fieldGoals, fieldGoalsAttempted, FT, FTA, blocksPerMinute, pointsPerMinute, stealsPerMinute, assistsPerMinute, turnoversPerMinute, tripleDoubles, doubleDoubles, threePP, offensiveReboundsPerMinute, defensiveReoundsPerMinute, fieldGoalP, FTP, usagePercentTot, offensiveRatingTot, defensiveRatingTot, trueShooting, effectiveFieldGoal)

        if key == 'guards':
            cursor.execute(insertTeamVsDefenseGuards, teamVsPlayerData)
        if key == 'fowards':
            cursor.execute(insertTeamVsDefenseFowards, teamVsPlayerData)

        cnx.commit()
def team_vs_defense_extrapolation(cursor, dates, teams, cnx):
    # iterate through all teams and all dates

    performanceAvgScript = "SELECT blocks, points, steals, assists, turnovers, totalRebounds, tripleDouble, doubleDouble, 3PM, 3PA, offensiveRebounds, defensiveRebounds, minutesPlayed, fieldGoals, fieldGoalsAttempted, FT, FTA, usagePercent, offensiveRating, defensiveRating, trueShootingPercent, effectiveFieldGoalPercent FROM performance WHERE opponent = %s AND dateID > %s AND dateID < %s AND fanduelPosition = %s"
    insertTeamVsDefenseGuards = "INSERT INTO team_vs_guards VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    insertTeamVsDefenseFowards = "INSERT INTO team_vs_fowards VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


    getLastID = "Select MAX(teamID) from team_vs_guards"
    cursor.execute(getLastID)
    try:
        tableID = int(cursor.fetchall()[0][0])
    except:
        tableID = 0
    tableID += 100


    beginningSeasonID = 0

    for date in dates:
        print date
        for team in teams:

            averaging(cursor, team, beginningSeasonID, date, tableID, performanceAvgScript, insertTeamVsDefenseGuards, insertTeamVsDefenseFowards, cnx)

            tableID = tableID + 1

if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()


   
    # get all teams
    getBbreffs = "SELECT bbreff FROM team_reference"
    cursor.execute(getBbreffs)

    teams = []

    sqlResults = cursor.fetchall()
    for row in sqlResults:
        teams.append(row[0])

    dateCutOff = constants.teamVsDefenseExtrapolationDateCutOff
    upperBoundCutOff = constants.extapolatorUpperBound

    getDates = "SELECT iddates FROM dates WHERE iddates >= %s AND iddates <= %s"
    getDatesD = (dateCutOff, upperBoundCutOff)
    cursor.execute(getDates, getDatesD)

    dates = []

    sqlResults = cursor.fetchall()
    for row in sqlResults:
        dates.append(row[0])
    
    team_vs_defense_extrapolation(cursor, dates, teams, cnx)

    cursor.close()
    cnx.commit()
    cnx.close()
