import mysql.connector


class SQL:
    def __init__(self, ):
        '''
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password"
        )
        self.mydb.autocommit(True)
        self.my_cursor = self.mydb.cursor()
        '''

    def load_classifications_by_time_frame(self, time_frame):
        # here will run a sql script or call stored procedure in mysql database
        # self.my_cursor.execute('''
        #     Select * from Classifications
        # ''')
        # classifications = self.my_cursor.fetchall()
        return 'this is just a test'
