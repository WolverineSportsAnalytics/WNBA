import requests
import csv
from bs4 import BeautifulSoup, Comment
from pydfs_lineup_optimizer import * # version >= 2.0.1
import datetime
from pytz import timezone

'''
Fanduel Scraper that scrapes rotogur for predicitions and optimizes lineups in place
'''


def predict():
    url = "https://www.rotowire.com/daily/mlb/optimizer.php?site=FanDuel&sport=mlb"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    games = soup.find("div",{"id":"rwo-matchups"}).find_all("div",{"class":"rwo-game-team"})
    zone = timezone("US/Eastern")
    now = datetime.datetime.now(tz=zone).time().strftime('%H:%M:%S')
    finished_games = []
    for game in games:
        team = game['data-team']
        time = game['data-gametimeonly']

        if now > time:
            finished_games.append(team)


    players = soup.find_all('tr')
    player_list = {}

    for i,count in zip(players[4:],range(len(players)-4)):
        try:
            name  = i.find_all('td')[1].text # name 
            names = name.split()
            name = names[0] + ' ' + names[1]
            
            
            team  = i.find_all('td')[2].text.rstrip()# team
            if team in finished_games:
                continue

            pos = i.find_all('td')[3].text # pos
            if pos == 'C1':
                pos = ['1B','C']
            else:
                pos = [str(pos)]
            sal = i.find_all('td')[6].find('input')['value']
            sal = sal[1:]
            sals = sal.split(",")
            sal = sals[0] + sals[1]
            rotoProj = i.find_all('td')[7].find('input')['value']



            player_list[names[0] + names[1]] = (Player(count, names[0], names[1], pos, team, float(sal), float(rotoProj), False))
        except Exception as e:
            print e

  
    url = "https://rotogrinders.com/projected-stats/mlb-pitcher.csv?site=fanduel"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for row in str(soup).split('\n')[:-1]:
        rows = row.split(",")
        names = rows[0][1:-1].split()
        pos = rows[3]
        team = rows[2]
        if team == "CHW":
            team = "CWS"
        if team in finished_games:
            continue
        sal = rows[1]
        rotoProj = rows[7]
        try:
            points = (player_list[names[0] + names[1]].fppg + float(rotoProj))/2
            player_list[names[0] + names[1]].fppg = points 
        except:
            pass

    url = "https://rotogrinders.com/projected-stats/mlb-hitter.csv?site=fanduel"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for row in str(soup).split('\n')[:-1]:
        rows = row.split(",")
        names = rows[0][1:-1].split()
        pos = rows[3]
        if pos == "C-1B":
            pos = ["C", "1B"]
        else:
            pos = [pos]
        team = rows[2]
        if team == "CHW":
            team = "CWS"
        if team in finished_games:
            continue
        sal = rows[1]
        rotoProj = rows[7]
        try:
            points = (player_list[names[0] + names[1]].fppg + float(rotoProj))/2
            player_list[names[0] + names[1]].fppg = points 
        except:
            pass


    p_list = []
    for _, p in player_list.items():
        p_list.append(p)
    
    optimizer = get_optimizer(Site.FANDUEL, Sport.BASEBALL)
    optimizer.load_players(p_list)

    numLineups = 5

    lineups = optimizer.optimize(n=numLineups, max_exposure=0.3)

    for lineup in lineups:
        print lineup
    return lineups

if __name__ == "__main__":

    predict()
