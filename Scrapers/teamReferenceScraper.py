import mysql.connector
from bs4 import BeautifulSoup
import requests
import constants


class wnbaTeam():
    def __init__(self, bbref, wsa, city, name):
        self.bbref = bbref
        self.wsa = wsa
        self.city = city
        self.name = name
    
    def insertTeam(self, cursor):
        insert_statement = "Insert into team_reference (bbreff, wsa, City, Name) Values(%s,%s,%s,%s)"
        inserts = (self.bbref, self.wsa, self.city, self.name)
        cursor.execute(insert_statement, inserts)
        


def insertTeams(cursor, cnx):
    Atlanta = wnbaTeam("ATL", "ATL", "Atlanta", "Dream")
    Atlanta.insertTeam(cursor)

    Chicago = wnbaTeam("CHI", "CHI", "Chicago", "Sky")
    Chicago.insertTeam(cursor)

    Connecticut = wnbaTeam("CON", "CON", "Connecticut", "Sun")
    Connecticut.insertTeam(cursor)

    Indiana = wnbaTeam("IND", "IND", "Indiana", "Fever")
    Indiana.insertTeam(cursor)

    LosAngelas = wnbaTeam("LAS", "LAS", "Los Angelas", "Sparks")
    LosAngelas.insertTeam(cursor)

    Minnesota = wnbaTeam("MIN", "MIN", "Minnesota", "Lynx")
    Minnesota.insertTeam(cursor)

    NewYork = wnbaTeam("NYL", "NYL", "New York", "Liberty")
    NewYork.insertTeam(cursor)
    
    Phoenix = wnbaTeam("PHO", "PHO", "Phoenix", "Mercury")
    Phoenix.insertTeam(cursor)

    LosVegas = wnbaTeam("LVA", "LVA", "Los Vegas", "Aces")
    LosVegas.insertTeam(cursor)

    Seattle = wnbaTeam("SEA", "SEA", "Seattle", "Storm")
    Seattle.insertTeam(cursor)

    Dallas = wnbaTeam("DAL", "DAL", "Dallas", "Wings")
    Dallas.insertTeam(cursor)

    Washington = wnbaTeam("WAS", "WAS", "Washington", "Mystics")
    Washington.insertTeam(cursor)

    cnx.commit()

def main():
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()

    insertTeams(cursor,cnx)

if __name__=="__main__":
    main()
