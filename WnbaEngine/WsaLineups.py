'''
 Wsa Lineup object that holds one baseball lineup
 Requeres players, date, time that lineup can be played before and projected points
'''
class WsaLineup():
    def __init__(self, players, date, slate, points, op_type):
        self.g1 = players[0]
        self.g2 = players[1]
        self.g3 = players[2]
        self.f1 = players[3]
        self.f2 = players[4]
        self.f3 = players[5]
        self.f4 = players[6]
        self.slate = slate
        self.date = date
        self.points = points
        self.op_type = op_type

    # insert each lineup with corresponding number into table
    def insertTable(self, cursor, lineupNumber):

        query = "Replace into lineups (lineupNumber, date, G1, G2, G3, F1, F2, F3, F4, slateName, projectedPoints, lineupType) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        inserts = (lineupNumber, self.date, self.g1, self.g2, self.g3, self.f1, self.f2, self.f3, self.f4, self.slate, self.points, self.op_type)
        cursor.execute(query, inserts)
