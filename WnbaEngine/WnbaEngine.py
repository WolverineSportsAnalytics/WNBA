import mysql.connector
from selenium import webdriver
import datetime
from bs4 import BeautifulSoup, Comment
import WsaLineups, WnbaOptimizer
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time, os
from django.core.cache import cache
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoSettings")
teamMap = {"LV" : "LVA"} 

class Slate():
    def __init__(self, teams, name):
        self.teams = teams
        self.name = name

class WsaEngine():
    def __init__(self):
        name = "WsaEngine"

    def get_slates(self):
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        browser = webdriver.Chrome(executable_path=("./chromedriver"),   chrome_options=chrome_options)
        
        url = "https://rotogrinders.com/lineuphq/wnba?site=fanduel"
        browser.get(url) #navigate to the page
        browser.find_element_by_id("slate-menu-link").click()
        time.sleep(3)
        page =browser.find_element_by_id("slate-select-menu").get_attribute("innerHTML")
        soup = BeautifulSoup(page, "html.parser")
        slates = soup.find_all("li",{"class": "slate-menu__slate"})
        
        slate_list = []
        for slate in slates:
            name = slate.find_all("b",{"class": "slate-menu__label"})[0].find("span").text
            games = slate.find_all("li",{"class": "slate-menu__game"})
            teams = []
            for game in games:
                split = game.find("span").text.split()
                if split[0] in teamMap:
                    teams.append(teamMap[split[0]])
                else:
                    teams.append(split[0])
                if split[2] in teamMap:
                    teams.append(teamMap[split[2]])
                else:
                    teams.append(split[2])

            if name != "All":
                slate_list.append(Slate(teams, name))
        
        browser.quit()
        self.slates = slate_list
    
    # Function to set lineups and insert into lineups table
    def setLineups(self, cursor, cnx, date):

        opt = WnbaOptimizer.WnbaOptimizer(date, cursor)
        opt.getPlayers(date)
        for slate in self.slates:
            opt.generateLineups("rotoWireProj", 1, date, time, slate)
            opt.insertLineups(cursor)
            opt.generateLineups("simmonsProj", 1, date, time, slate)
            opt.insertLineups(cursor)

        cnx.commit()

    def getAllLineups(self, cursor, date):

        query = "Select * from lineups where date=%s"
        cursor.execute(query, (date,) )
        fetchedLineups = cursor.fetchall()
        lineups = []
        for line in fetchedLineups:
            lineups.append(WsaLineups.WsaLineup(line[2:9], line[1], line[9], line[10], line[11]))
        return lineups

def getWsaLineups():

    cnx = mysql.connector.connect(user="wsa@wsabasketball",
                host='wsabasketball.mysql.database.azure.com',
                database="wnba",
                password="LeBron>MJ!")                                                                                                               
    cursor = cnx.cursor()
        
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    gen = WsaEngine() 
    gen.get_slates()
    gen.setLineups(cursor,cnx, today)
    lineups = gen.getAllLineups(cursor, today)
    cache.set("WnbaLineups", lineups)

if __name__=="__main__":
    getWsaLineups()
