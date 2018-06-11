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

def fixFanduelIDs(cursor):
    getFDIds = "select playerID, fanduelID FROM player_reference WHERE fanduelID IS NOT NULL"
    cursor.execute(getFDIds)

    insertFDIds = "UPDATE player_reference SET fanduelID = %s WHERE playerID = %s"

    results = cursor.fetchall()

    for player in results:
        fdID = player[1]
        pID = player[0]
        if fdID.find("-") != -1:
            fdDate, actualFDID = fdID.split("-")

            insertFDIdsD = (actualFDID, pID)
            cursor.execute(insertFDIds, insertFDIdsD)

            cnx.commit()

def alignPlayerIDs(cursor):
    selec_id = "select playerID from player_reference where firstName= %s and lastName = %s"
    select_idTwo = "SELECT playerID from player_reference where nickName=%s"

    insertRotoguruID = "UPDATE player_reference SET fanduelID = %s WHERE playerID = %s"

    with open(constants.fanduelFileLocation, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        i = 0
        for row in reader:
            # if they don't play don't consider them
            firstName = row[3]
            firstName = firstName.strip()
            lastName = row[5]
            lastName = lastName.strip()
            selectData = (firstName, lastName)
            cursor.execute(selec_id, selectData)
            if not cursor.rowcount:
                name = row[4]
                nameData = (name,)
                cursor.execute(select_idTwo, nameData)
                if cursor.rowcount:
                    playerID = 0
                    for id in cursor:
                        playerID = id[0]
                    insertData = (row[1].strip(), playerID)
                    cursor.execute(insertRotoguruID, insertData)
                    cnx.commit()
                else:
                    print "Must manual insert fanduel id for: " + name
            else:
                playerID = 0
                for id in cursor:
                    playerID = id[0]
                insertData = (row[1].strip(), playerID)
                cursor.execute(insertRotoguruID, insertData)
                cnx.commit()

    cursor.close()
    cnx.commit()
    cnx.close()

def insert_into_performance(cursor, cnx, dateID):
    #empty will be used to scrape from rotoguru csv

    getPlayerID = "select playerID from player_reference where nickName= %s"

    getTeamAbbrev = "SELECT wsa from team_reference where fanduel = %s"
    update_performance = "INSERT INTO performance (playerID, dateID, fanduel, team, opponent, fanduelPosition) VALUES (%s, %s, %s, %s, %s, %s)"


    url = "https://www.rotowire.com/daily/wnba/optimizer.php?site=FanDuel&sport=wnba"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    players = soup.find("tbody", {"id": "players"}).find_all('tr')


    for i in players:
        name  = i.find_all('td')[1].text # name 
        names = name.split()
        name = names[0] + ' ' + names[1]
        print name
        pos = i.find_all('td')[4].text # pos
        print pos
        sal = i.find_all('td')[15].find('input')['value']
        sal = sal[1:]
        sals = sal.split(",")
        sal = sals[0] + sals[1]
        print sal
        team = i.find_all('td')[2].text
        opp = i.find_all('td')[3].text
        getPlayerIDD = (name, )
        cursor.execute(getPlayerID, getPlayerIDD)

        if not cursor.rowcount:                    
          print ("Did not insert into performance table for " + name)

        else:
          try:
              player_id = cursor.fetchall()[0][0]
              print player_id

              # insert into the performance table
              inserts = (
              player_id,
              dateID,
              sal,
              team,
              opp,
              pos)

              cursor.execute(update_performance, inserts)
              print update_performance, inserts

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
    
    #dateID = getDate(constants.dayP, constants.monthP, constants.yearP, cursor)
    dateID = getDate(10, 6, 2018, cursor)

    insert_into_performance(cursor, cnx, dateID)

    cursor.close()
    cnx.commit()
    cnx.close()




