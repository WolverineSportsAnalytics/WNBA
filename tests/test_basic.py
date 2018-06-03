# this is the first of our testing files so that we can keep everything all Up and running
import unittest
import constants
import mysql.connector

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
        def setUpModule(self):
            self.cnx = mysql.connector.connect(user=constants.testUser,
                host=constants.testHost,
                database=constants.testName,
                password=constants.testPassword)                                                                                                               
            self.cusror = cnx.cursor()

        def testInsertAndRetrival(self):
            insert_statement = "Insert into playerReferece values" 

            self.assertEqual(1, 1)

        def tearDownModule():
            clear_table = "delete from playerReferece"
            

    



if __name__ == '__main__':
    unittest.main()
