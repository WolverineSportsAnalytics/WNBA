# this will bootstrap a full test database up to date with todays data
import os
import constants
from Scrapers import generateDates, playerReferenceScraper, positionScraper, teamReferenceScraper, generateBoxScoreUrls, teamPerformanceScraper, performanceScraper
from Extrapilators import dailyPerformanceExtrapilator, teamPerformanceExtrapilator, teamVsDefenseExtrapilator
import mysql.connector
import datetime

def main():
    os.system("mysql -u root < tests/create_data.sql")
   
    now = datetime.datetime.now()
    cnx = mysql.connector.connect(user=constants.testUser,
                                  host=constants.testHost,
                                  database=constants.testName,
                                  password=constants.testPassword)
    cursor = cnx.cursor()

    # generateDates.generatedates(18, 5, 2018, 18, 9, 2018, cursor)
    # cnx.commit()
    # playerReferenceScraper.scrapeHtml(cursor,cnx)
    # positionScraper.insert_into_performance(cursor, cnx)
    # teamReferenceScraper.insertTeams(cursor,cnx)
    # dates = generateBoxScoreUrls.generateDates(18, 5, 2018, now.day, now.month, now.year)
    # generateBoxScoreUrls.generateUrls(cursor, cnx, dates)
    # performanceScraper.updateAndInsertPlayerRef(18, 5, 2018, now.day, now.month, now.year, cursor, cnx)
    # teamPerformanceScraper.updateAndInsertPlayerRef(18, 5, 2018, now.day, now.month, now.year, cursor, cnx)
    today = generateBoxScoreUrls.findDate(now.year, now.month, now.day, cursor)
    # dailyPerformanceExtrapilator.extrapolate(0, today, cursor, cnx)
    # teamPerformanceExtrapilator.extrapolate(0, today, cursor, cnx)
    os.system("mysql - root < Scrapers/setPerformancePos.sql")
    teamVsDefenseExtrapilator.extrapolate(0, today, cursor, cnx)



    

if __name__=='__main__':
    main()
