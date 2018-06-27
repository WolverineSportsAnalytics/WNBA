# this will bootstrap a full test database up to date with todays data
import os
import constants
from Scrapers import generateDates, playerReferenceScraper, positionScraper, teamReferenceScraper, generateBoxScoreUrls, teamPerformanceScraper, performanceScraper
from Extrapilators import dailyPerformanceExtrapilator, teamPerformanceExtrapilator, teamVsDefenseExtrapilator
from Optimization import sumPoints, featuresFiller 
import mysql.connector
import datetime

def main():
    if constants.testPassword != "":
        string = "mysql -h " + constants.testHost + " -u " + constants.testUser + " -p\"" + constants.testPassword + "\" < tests/create_data.sql"
        os.system(string)
    else:
        os.system("mysql -u " + constants.testUser + " < tests/create_data.sql")
   
    now = datetime.datetime.now()
    cnx = mysql.connector.connect(user=constants.testUser,
                                  host=constants.testHost,
                                  database=constants.testName,
                                  password=constants.testPassword)
    cursor = cnx.cursor()

    # check if performance is empty if not dont bootstrap
    cursor.execute("Select count(*) from performance")
    if cursor.fetchall()[0][0] != 0:
       print "Performance not empty can't bootstrap"
       return 
    generateDates.generatedates(18, 5, 2018, 18, 9, 2018, cursor)
    cnx.commit()
    playerReferenceScraper.scrapeHtml(cursor,cnx)
    positionScraper.insert_into_performance(cursor, cnx)
    teamReferenceScraper.insertTeams(cursor,cnx)
    dates = generateBoxScoreUrls.generateDates(18, 5, 2018, now.day, now.month, now.year)
    generateBoxScoreUrls.generateUrls(cursor, cnx, dates)
    performanceScraper.updateAndInsertPlayerRef(18, 5, 2018, now.day, now.month, now.year, cursor, cnx)

    try:
        cursor.clos()
        cnx.commit()
        cnx.close()
    except:
        pass

    cnx = mysql.connector.connect(user=constants.testUser,
                                  host=constants.testHost,
                                  database=constants.testName,
                                  password=constants.testPassword)
    cursor = cnx.cursor()

    teamPerformanceScraper.updateAndInsertPlayerRef(18, 5, 2018, now.day, now.month, now.year, cursor, cnx)
    today = generateBoxScoreUrls.findDate(now.year, now.month, now.day, cursor)
    dailyPerformanceExtrapilator.extrapolate(0, today, cursor, cnx)
    teamPerformanceExtrapilator.extrapolate(0, today, cursor, cnx)
    teamVsDefenseExtrapilator.extrapolate(0, today, cursor, cnx)
    sumPoints.auto(today, cursor) 
    cursor.execute("update performance set projMinutes=minutesPlayed where projMinutes is null")
    cnx.commit()
    featuresFiller.fill(now.year, now.month, now.day, today, cursor, cnx)
    cursor.close()
    cnx.commit()
    cnx.close()
    

if __name__=='__main__':
    main()
