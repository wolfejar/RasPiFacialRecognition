import mysql.connector
from models.classification import Classification
from models.user import OwnerUser, GuestUser


class SQL:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="password",
            database="FacialRecognitionApp",
            autocommit=True
        )
        self.my_cursor = self.mydb.cursor()

    def load_model_classifications_by_time_frame(self, model_id, time_frame):
        # here will run a sql script or call stored procedure in mysql database
        self.my_cursor.execute('''
            Select * 
            from Model M
            JOIN ModelUserClassification MUC on MUC.ModelId = M.ModelId
            where M.ModelId = {} and MUC.ClassificationTimestamp > '{}'
        '''.format(model_id, time_frame))

        classifications = self.my_cursor.fetchall()
        print(classifications)

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
        self.my_cursor.execute(
            '''
            SELECT U.HashedPassword
            From AppUser U
            Where U.Username = '{}'
            '''.format(username))
        row = self.my_cursor.fetchone()
        if row is None:
            return None
        return row[0]

    def create_account(self, username, password, first_name, last_name, role):
        self.my_cursor.execute(
            '''
            INSERT INTO AppUser(UserName, HashedPassword, FirstName, LastName, Role)
            Values ('{}', '{}', '{}', '{}', '{}');
            '''.format(username, password, first_name, last_name, role))
