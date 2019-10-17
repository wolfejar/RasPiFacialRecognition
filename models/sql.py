import mysql.connector


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

    def get_user_id(self, username):
        self.my_cursor.execute(
            '''
            Select U.UserId
            From AppUser U
            WHERE U.username = '{}'
            '''.format(username))
        return self.my_cursor.fetchone()[0]

    def load_model_classifications_by_time_frame(self, model_id, time_frame):
        # here will run a sql script or call stored procedure in mysql database
        self.my_cursor.execute('''
            Select * 
            from Model M
            JOIN ModelUserClassification MUC on MUC.ModelId = M.ModelId
            where M.ModelId = {} and MUC.ClassificationTimestamp > '{}'
        '''.format(model_id, time_frame))

        classifications = self.my_cursor.fetchall()

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
        user_id = self.get_user_id(username)
        self.my_cursor.execute(
            '''
            UPDATE AppUser
            SET HomeUserId = '{}'
            WHERE username = '{}'
            '''.format(user_id, username)
        )

    def get_friends(self, username):
        user_id = self.get_user_id(username)
        self.my_cursor.execute('''
            Select *
            From AppUser U
            Where U.HomeUserId = '{}' and U.UserId != '{}'
        '''.format(user_id, user_id))
        rows = self.my_cursor.fetchall()
        print(rows)
        return rows
