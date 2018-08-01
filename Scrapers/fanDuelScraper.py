# will hopefully scrape a site other than fanduel for salaries and matchups daily
import mysql.connector
import datetime
import constants
import csv
import traceback
from datetime import date
import urllib2
import requests
from bs4 import BeautifulSoup, Comment
import json

'''
Fanduel scraper scrapes the fanduel csv and inserts into the performance table
'''

def getDate(day, month, year, cursor):
    findGame = 'SELECT iddates FROM dates WHERE date = %s'
    findGameData = (date(year, month, day),)
    cursor.execute(findGame, findGameData)

    dateID = -1
    for datez in cursor:
        dateID = datez[0]

    return dateID

def insert_into_performance(cursor, cnx, dateID):
    #empty will be used to scrape from rotoguru csv

    getPlayerID = "select playerID from player_reference where nickName= %s"
    getPlayerbyfirstandTeam = "select playerID from player_reference where firstName= %s and team=%s"
    getPlayerbylastandTeam = "select playerID from player_reference where lastName= %s and team=%s"

    getTeamAbbrev = "SELECT wsa from team_reference where fanduel = %s"
    update_performance = "INSERT INTO performance (playerID, dateID, fanduel, team, opponent, fanduelPosition, projMinutes, rotowireProj) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    url = "https://www.rotowire.com/daily/tables/optimizer-wnba.php?sport=WNBA&site=FanDuel&projections=&type=main&slate=Main"
    page = requests.get(url)
    players = json.loads(page.text)
    
    for player in players:

        first_name = player['first_name'] 
        last_name = player['last_name']
        name = first_name + ' ' + last_name
        
	team  = player['team'] 
        if team == "NY":
            team = "NYL"
        if team == "LAV":
            team = "LVA"
        if team == "LA":
            team = "LAS"

	pos = player['position']
        sal = player['salary']
        rotoProj = player['proj_rotowire']
        minutes = player['minutes']
	opp  = player['opponent'] 
	if opp == "NY":
            opp = "NYL"
        if opp == "LAV":
            opp = "LVA"
        if opp == "LA":
            opp = "LAS"
	
        getPlayerIDD = (name, )
        cursor.execute(getPlayerID, getPlayerIDD)
        player_id = cursor.fetchall()
  
        if not len(player_id):                    

            getPlayerIDD = (first_name, team )
            cursor.execute(getPlayerbyfirstandTeam, getPlayerIDD)
            player_id = cursor.fetchall()
            
            if not len(player_id):
                getPlayerIDD = (last_name, team )
                cursor.execute(getPlayerbylastandTeam, getPlayerIDD)
                player_id = cursor.fetchall()

                if not len(player_id):
                    print ("Did not insert into performance table for " + name)
                else: 
                    found = True
            else:
                found = True
        else:
            found = True

        if found:
          try:
              player_id = player_id[0][0]

              # insert into the performance table
              inserts = (
              player_id,
              dateID,
              sal,
              team,
              opp,
              pos,
              minutes,
              rotoProj,
              )

              cursor.execute(update_performance, inserts)

          except:
              # traceback.print_exc()
              print name, "Not inserted"

          cnx.commit()

    return 0

if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()
    
    #dateID = getDate(constants.dayP, constants.monthP, constants.yearP, cursor)
    dateID = getDate(13, 6, 2018, cursor)
    print dateID

    insert_into_performance(cursor, cnx, dateID)

    cursor.close()
    cnx.commit()
    cnx.close()



