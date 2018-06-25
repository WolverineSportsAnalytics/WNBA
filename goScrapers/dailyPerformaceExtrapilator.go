package main

import (
        "database/sql"
        _ "github.com/go-sql-driver/mysql"
	"fmt"
)

func player_total_avg(db *sql.DB) {
        const average = "select avg(blocks), avg(points), avg(steals), avg(assists), avg(turnovers), avg(totalRebounds), avg(tripleDouble), avg(doubleDouble), avg(3PM), avg(offensiveRebounds), avg(defensiveRebounds), avg(minutesPlayed), avg(fieldGoals), avg(fieldGoalsAttempted), avg(fieldGoalPercent), avg(3PA), avg(3PPercent), avg(FT), avg(FTA), avg(FTPercent), avg(personalFouls), avg(plusMinus), avg(trueShootingPercent), avg(effectiveFieldGoalPercent), avg(freeThrowAttemptRate), avg(3pointAttemptRate), avg(offensiveReboundPercent), avg(defensiveReboundPercent), avg(totalReboundPercent), avg(assistPercent), avg(stealPercent), avg(blockPercent), avg(turnoverPercent), avg(usagePercent), avg(offensiveRating), avg(defensiveRating) from performance where playerID=144 and dateID>0 and dateID < 23"


        rows, _ := db.Query(average)
	var avg string
	rows.Scan(&avg)
	if rows.Next() {
		rows.Scan(&avg)
		fmt.Print(avg)
	}

}

//main
func main(){
        // currently only connecting to test db
        db, err :=sql.Open("mysql","root:@/wnba_test")
        defer db.Close()
        err = db.Ping()

        if err != nil {
                    panic(err.Error())
        }
        player_total_avg(db)

}

