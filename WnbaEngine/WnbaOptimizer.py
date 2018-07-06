from pydfs_lineup_optimizer import * # version >= 2.0.1
import datetime
import WsaLineups

''' Object that with optimize and insert lineups into database 
    Takes a database connection cursor and date as paremeters 
    Requires that the playes table has been prepopulated     '''

def getDateId(date, cursor):
    cursor.execute("Select iddates from dates where date=\"" + date+ "\"")
    return cursor.fetchall()[0][0] -1

class WnbaOptimizer():
    def __init__(self, date, cursor):
        self.cursor = cursor
        self.getPlayers(date)
        self.my_lineups = []
    
    def getPlayers(self, date):
        dateID = getDateId(date, self.cursor)
        query = "SELECT b.nickName, p.playerID, p.fanduelPosition, p.simmonsProj, p.rotowireProj, p.team, p.fanduel, p.opponent, p.fanduelPts FROM performance as p LEFT JOIN player_reference as b ON b.playerID = p.playerID WHERE p.dateID = %s AND p.projMinutes >= 8 AND p.fanduel > 0 AND p.rotowireProj IS NOT NULL AND p.rotowireProj > 0"
 
        self.cursor.execute(query, (dateID,))
        self.players = self.cursor.fetchall()

    def generateLineups(self, op_type, numLineups, date, time, slate):
        opt_players = []
        count = 0
        for player in self.players:
            if player[5] in slate.teams: 
                # if proj is null
                proj = player[3]
                if op_type =="simmonsProj":
                    proj = player[3]
                elif op_type =="rotoWireProj":
                    proj = player[4]
                
                opt_players.append(Player(player[1],player[0], "", player[2].split("/"), player[5], float(player[6]), float(proj), False))
                count+=1


        optimizer = get_optimizer(Site.FANDUEL, Sport.WNBA)
        optimizer.load_players(opt_players)

        lineups = optimizer.optimize(n=numLineups, max_exposure=0.3)
        for lineup in lineups:
            sublineup = []
            for player in lineup.players:
                sublineup.append(player.first_name)
            points = lineup.fantasy_points_projection
            self.my_lineups.append(WsaLineups.WsaLineup(sublineup, date, slate.name, points, op_type))

    
    def insertLineups(self, cursor):
        count = 1 
        for lineup in self.my_lineups:
            lineup.insertTable(cursor, count)
            count += 1
        self.my_lineups = []

