# this will bootstrap a full test database up to date with todays data
import os
import constants
from Scrapers import generateDates, playerReferenceScraper, positionScraper, teamReferenceScraper, generateBoxScoreUrls, teamPerformanceScraper, performanceScraper
from Extrapilators import dailyPerformanceExtrapilator, teamPerformanceExtrapilator, teamVsDefenseExtrapilator
from Optimization import sumPoints, featuresFiller, Optimizer, projectMagic, train
import mysql.connector
import datetime
import time

def make_connection():
     try:
        cnx = mysql.connector.connect(user=constants.testUser,
                                  host=constants.testHost,
                                  database=constants.testName,
                                  password=constants.testPassword,
                                  )
        cursor = cnx.cursor()
        return cnx, cursor
     except Exception as e:
        print e
        time.sleep(30)
        return make_connection()

def main():
    now = datetime.datetime.now()
           
    cnx, cursor = make_connection()
    print "We in"

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

    # fill in projections for previous days
    train.train(today-1, cursor, cnx) 
    for days in range(today):
        try:
            projectMagic.actualProjMagic(day, cursor, cnx)
        except:
            pass

    cursor.close()
    cnx.commit()
    cnx.close()
    

if __name__=='__main__':
    main()
