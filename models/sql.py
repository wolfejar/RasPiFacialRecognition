import mysql.connector
from models.classification import Classification
from models.user import OwnerUser, GuestUser


class SQL:
    def __init__(self):
        '''
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password"
        )
        self.mydb.autocommit(True)
        self.my_cursor = self.mydb.cursor()
        '''

    def load_model_classifications_by_time_frame(self, model_id, time_frame):
        # here will run a sql script or call stored procedure in mysql database
        # self.my_cursor.execute('''
        #     Select * from Classifications
        # ''')
        # classifications = self.my_cursor.fetchall()

        # sql will load OwnerUser and GuestUser objects and other classification data based on time frame from MySQL
        users = [OwnerUser(12345, 'Jim', 'Smith'),
                 GuestUser(12346, 'Joe', 'Doe'),
                 GuestUser(12347, 'Jeff', 'Tate')]
        classifications = [
            Classification(friends=users, output=[0.87, 0.13, 0.05], timestamp='11/21/2019'),
            Classification(friends=users, output=[0.14, 0.98, 0.23], timestamp='11/22/2019'),
            Classification(friends=users, output=[0.07, 0.33, 0.91], timestamp='11/23/2019')]
        return classifications

    def get_hashed_pass(self, username):
        '''
        :param username:
        :return:
        self.my_cursor.execute(
            SELECT S.HashedPass
            From Student S
            Where S.Email = '{}'
        .format(email))
        row = self.my_cursor.fetchone()
        if row is None:
            return None
        return row[0]'''
        return None
