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

def insert_into_performance(cursor, cnx):
    #empty will be used to scrape from rotoguru csv

    getPlayerID = "select playerID from player_reference where nickName= %s"
    getPlayerbyfirstandTeam = "select playerID from player_reference where firstName= %s and team=%s"
    getPlayerbylastandTeam = "select playerID from player_reference where lastName= %s and team=%s"
    

    updateStatement = "Update player_reference set pos = %s where playerID = %s"


    url = "https://www.rotowire.com/wnba/player-stats-byseason.php"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    players = soup.find("div", {"class": "span49"}).find_all('tbody')
    players = soup.find_all('tbody')[0].find_all('tr')


    for i in players:
        name  = i.find_all('td')[0].text # name 
        names = name.split()
        name = names[0] + ' ' + names[1]
        team = i.find_all('td')[1].text
        if team == "NY":
            team = "NYL"
        if team == "LAV":
            team = "LVA"
        pos = str(i.find_all('td')[2].text).rstrip()
        if pos=="C":
            pos = "F"
        getPlayerIDD = (name, )
        cursor.execute(getPlayerID, getPlayerIDD)

        player_id = cursor.fetchall()
        found = False
        if not len(player_id):                    

            getPlayerIDD = (names[0], team )
            print getPlayerIDD
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
                      pos,
                      player_id,
              )

              cursor.execute(updateStatement, inserts)
          except:
              traceback.print_exc()
              print name

          cnx.commit()

if __name__ == "__main__":
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()
    
    insert_into_performance(cursor, cnx)

    cursor.close()
    cnx.commit()
    cnx.close()




