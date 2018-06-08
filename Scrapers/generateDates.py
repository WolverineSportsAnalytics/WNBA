import mysql.connector
from datetime import timedelta, date
import constants

def generatedates(startDay, startMonth, startYear, endDay, endMonth, endYear, cursor):
    date_statement = 'DECLARE @date date = '	
    insert = "INSERT into dates(date) VALUES(%s)"
    start_date = date(startYear, startMonth, startDay)
    end_date = date(endYear, endMonth, endDay)
    for single_date in daterange(start_date, end_date):
	    dates =  str(single_date.year) + '-' + str(single_date.month) + '-' + str(single_date.day)
	    new_date = date_statement + "\'" + dates +"\';" 
	    date_stat = (dates,) 
	    cursor.execute(insert, date_stat)
	    print new_date

# function to iterate through a range of dates in the scrapers
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":
    print("Generate")
    cnx = mysql.connector.connect(user=constants.testUser,
            host=constants.testHost,
            database=constants.testName,
            password=constants.testPassword)                                                                                                               
    cursor = cnx.cursor()

    generatedates(constants.startDayP, constants.startMonthP, constants.startYearP, constants.endDayP, constants.endMonthP, constants.endYearP,cursor)

    cursor.close()
    cnx.commit()
    cnx.close()
