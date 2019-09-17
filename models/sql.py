import mysql.connector

class SQL:
    def __init__(self, ):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="yourusername",
            passwd="yourpassword"
        )
        self.mydb.autocommit(True)
        self.my_cursor = self.mydb.cursor()

    def fetch_classifications_by_time_frame(self, time_frame):
        return