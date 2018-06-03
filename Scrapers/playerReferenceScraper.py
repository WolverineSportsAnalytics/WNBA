#This file will scrap to get the names of all the WNBA players and put into playerReference Table
# Basektball reference does not have daily leaders for wnba so will scrape from the team section
# https://www.basketball-reference.com/wnba/teams/{{ team }}/2018.html

import mysql.connector
from bs4 import BeautifulSoup
import requests
import constants

team_abrev = ["ATL", "CHI", "CON", "IND", "LAS", "MIN", "NYL", "PHO", "LVA", "SEA", "DAL", "WAS"] 
def generateURLs():
    urls = []
    for team in team_abrev:
        urls.append(["https://www.basketball-reference.com/wnba/teams/" + team + "/2018.html", team])

    return urls

class PlayerRefObject():
    def __init__(self, name, team, bbref):
        self.name = name
        self.team = team
        self.bbref = bbref

    def add_to_table(self, cursor, cnx):
        addPlayer = "INSERT INTO player_reference (nickName, bbrefID, firstName, lastName, team) VALUES(%s, %s, %s, %s, %s)"
        payload = (self.name, self.bbref, self.name.split()[0], " ".join(self.name.split()[1:]), self.team)

        cursor.execute(addPlayer, payload)
        cnx.commit()


def scrapeHtml(cursor, cnx):
    urls = generateURLs()
    
    for url in urls:
        page = requests.get(url[0])
        soup = BeautifulSoup(page.text, 'html.parser')

        tables = soup.find_all("table")
        players_table = tables[1]
        rows = players_table.find_all("tr")
        for tr in rows[1:]:
                row = tr.find_all("td")[0]
                name = row.a.text
                bbref = row['data-append-csv']
                team = url[1]
                player = PlayerRefObject(name, team, bbref)
                player.add_to_table(cursor,cnx)


        

def main():
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()

    scrapeHtml(cursor,cnx)

if __name__=="__main__":
    main()
