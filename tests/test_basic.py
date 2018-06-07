# this is the first of our testing files so that we can keep everything all Up and running
import unittest
import constants
import mysql.connector
import sys
from os import path
sys.path.append("Scrapers" )
sys.path.append("../Scrapers" )
import playerReferenceScraper

class TestBasic(unittest.TestCase):

    def test(self):
        self.assertEqual(1, 1)

class TestDataBaseConnection(unittest.TestCase):

    def test_connect(self):
         try:
            cnx = mysql.connector.connect(user=constants.testUser,
                host=constants.testHost,
                database=constants.testName,
                password=constants.testPassword)                                                                                                               
            cusror = cnx.cursor()
            self.assertEqual(1, 1)
         except :
            self.assertEqual(0, 1)


class TestPlayerReference(unittest.TestCase):
        def setUp(self):
            self.cnx = mysql.connector.connect(user=constants.testUser,
                host=constants.testHost,
                database=constants.testName,
                password=constants.testPassword)                                                                                                               
            self.cursor = self.cnx.cursor()

        def testInsertAndRetrival(self):
            insert_statement = "Insert into player_reference (playerID, playerName) values (%s, %s)" 
            objects = ("1", "Evan Ciancio")
            
            self.cursor.execute(insert_statement, objects)
            self.cnx.commit()

            select = "Select playerName from player_reference where playerID = 1"
            self.cursor.execute(select)
            name = str(self.cursor.fetchall()[0][0])

            self.assertEqual(name , "Evan Ciancio")

        def tearDown(self):
            clear_table = "delete from player_reference"
            self.cursor.execute(clear_table)
            self.cnx.commit()
            

    



if __name__ == '__main__':
    unittest.main()
