# will hopefully scrape a site other than fanduel for salaries and matchups daily
import mysql.connector
import constants
import csv
import traceback
from datetime import date
import urllib2
import requests
from bs4 import BeautifulSoup, Comment

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

    url = "https://www.rotowire.com/daily/wnba/optimizer.php?site=FanDuel&sport=wnba"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    players = soup.find("tbody", {"id": "players"}).find_all('tr')


    for i in players:
        name  = i.find_all('td')[1].text # name 
        names = name.split()
        name = names[0] + ' ' + names[1]
        
        team  = i.find_all('td')[2].text.rstrip()# team
        if team == "NY":
            team = "NYL"
        if team == "LAV":
            team = "LVA"
        if team == "LA":
            team = "LAS"

        pos = i.find_all('td')[4].text # pos
        sal = i.find_all('td')[15].find('input')['value']
        sal = sal[1:]
        sals = sal.split(",")
        sal = sals[0] + sals[1]
        minutes = i.find_all('td')[6].text
        rotoProj = i.find_all('td')[16].find('input')['value']
        opp = i.find_all('td')[3].text
        getPlayerIDD = (name, )
        cursor.execute(getPlayerID, getPlayerIDD)
        player_id = cursor.fetchall()
  
        if not len(player_id):                    

            getPlayerIDD = (names[0], team )
            cursor.execute(getPlayerbyfirstandTeam, getPlayerIDD)
            player_id = cursor.fetchall()
            
            if not len(player_id):
                getPlayerIDD = (names[1], team )
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



