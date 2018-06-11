package main

import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
	"strings"
	"net/http"
	"golang.org/x/net/html"
)


var teams = []string{"ATL", "CHI", "CON", "IND", "LAS", "MIN", "NYL", "PHO", "LVA", "SEA", "DAL", "WAS"}

// player struct
type Player struct {
	bbrefid string
	nickName string
	team string
}

//method to add to table
func (p Player) add_to_table(db *sql.DB) {
	sep := strings.Split(p.nickName, ",")
	first := sep[1]
	last := sep[0]
        const addPlayer = "INSERT INTO player_reference (nickName, bbrefID, firstName, lastName, team) VALUES(?,?,?,?,?)"
	_, err := db.Exec(addPlayer, first + " " + last,p.bbrefid, first, last, p.team)
	if err != nil {
		panic(err.Error())
	}
}

// scape Html page for tam
func scrapeHtml(url string, team string, db *sql.DB) {
	resp, _ := http.Get(url)

	z := html.NewTokenizer(resp.Body)
	scrape:for {
		tt := z.Next()
		switch {
			case tt == html.ErrorToken:
				// End of the document, we're done

				break scrape
			case tt == html.StartTagToken:
				t := z.Token()
				isTable := t.Data == "td"
				if isTable {
					if t.Attr[1].Key == "data-append-csv"{
						p := Player{t.Attr[1].Val, t.Attr[3].Val, team}
						p.add_to_table(db)
					}
				}
			}
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

	var url string
	for _, team := range teams {
		url = "https://www.basketball-reference.com/wnba/teams/" + team + "/2018.html"
		scrapeHtml(url, team, db)
	}
}

