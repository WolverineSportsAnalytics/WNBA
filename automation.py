#!/usr/bin/python

# this will automate everything to be ran in one quick command daily
import os
import constants
from Scrapers import generateDates, playerReferenceScraper, positionScraper, teamReferenceScraper, generateBoxScoreUrls, teamPerformanceScraper, performanceScraper, fanDuelScraper
from Extrapilators import dailyPerformanceExtrapilator, teamPerformanceExtrapilator, teamVsDefenseExtrapilator
from Optimization import sumPoints, featuresFiller, Optimizer, projectMagic, train
from WnbaEngine import WnbaEngine
import mysql.connector
import datetime

def main():
    now = datetime.datetime.now()
    yesterday = now - datetime.timedelta(days=1)
    cnx = mysql.connector.connect(user=constants.testUser,
                                  host=constants.testHost,
                                  database=constants.testName,
                                  password=constants.testPassword)
    cursor = cnx.cursor()
    dates = generateBoxScoreUrls.generateDates(yesterday.day, yesterday.month, yesterday.year, now.day, now.month, now.year)
    print dates
    generateBoxScoreUrls.generateUrls(cursor, cnx, dates)
    performanceScraper.updateAndInsertPlayerRef(yesterday.day, yesterday.month, yesterday.year, now.day, now.month, now.year, cursor, cnx)

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

    teamPerformanceScraper.updateAndInsertPlayerRef(yesterday.day, yesterday.month, yesterday.year, now.day, now.month, now.year, cursor, cnx)
    today = generateBoxScoreUrls.findDate(now.year, now.month, now.day, cursor)
    
    dailyPerformanceExtrapilator.extrapolate(today, today, cursor, cnx)
    teamPerformanceExtrapilator.extrapolate(today, today, cursor, cnx)
    teamVsDefenseExtrapilator.extrapolate(today, today, cursor, cnx)
    sumPoints.auto(today, cursor) 
    cursor.execute("update performance set projMinutes=minutesPlayed where projMinutes is null")
    cnx.commit()
    today = generateBoxScoreUrls.findDate(now.year, now.month, now.day, cursor)
    status = fanDuelScraper.insert_into_performance(cursor, cnx, today)

    if status == 0:
        featuresFiller.fill(now.year, now.month, now.day, 1, cursor, cnx)
        train.train(today-1, cursor, cnx) 
        projectMagic.actualProjMagic(today, cursor, cnx)
        Optimizer.optimize(now.day, now.month, now.year, cursor, "simmonsProj")
        os.chdir("WnbaEngine")
        WnbaEngine.getWsaLineups()

    cursor.close()
    cnx.commit()
    cnx.close()
    

if __name__=='__main__':
    main()
