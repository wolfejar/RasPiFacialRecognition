import mysql.connector


class SQL:
    def __init__(self):
        with open('./static/db_credentials.txt') as f:
            user = f.readline()
            passwd = f.readline()
        self.mydb = mysql.connector.connect(
            host="localhost",
            user=user,
            passwd=passwd,
            database="FacialRecognitionApp",
            autocommit=True
        )
        self.my_cursor = self.mydb.cursor(buffered=True)

    def get_user_id(self, home_username, username):
        self.my_cursor.execute(
            '''
            Select U.UserId
            From AppUser U
            WHERE U.UserName = '{}'
            '''.format(home_username))
        home_user_id = self.my_cursor.fetchone()[0]
        self.my_cursor.execute(
            '''
            Select U.UserId
            From AppUser U
            WHERE U.UserName = '{}' and U.HomeUserId = '{}'
            '''.format(username, home_user_id))
        return self.my_cursor.fetchone()[0]

    def get_new_account_user_id(self, new_username):
        self.my_cursor.execute(
            '''
            Select U.UserId
            From AppUser U
            WHERE U.UserName = '{}'
            '''.format(new_username)
        )
        return self.my_cursor.fetchone()[0]

    def load_model_classifications_since_time_stamp(self, model_id, time_stamp):
        self.my_cursor.execute('''
            Select MUC.UserId, MUC.firstname, MUC.lastname, MUC.confidence, MUC.classificationtimestamp, MUC.imagepath
            from Model M
            JOIN ModelUserClassification MUC on MUC.ModelId = M.ModelId
            where M.ModelId = {} and MUC.ClassificationTimestamp > '{}'
        '''.format(model_id, time_stamp))

        return self.my_cursor.fetchall()

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

    def create_account(self, username, password, first_name, last_name):
        self.my_cursor.execute(
            '''
            INSERT INTO AppUser(UserName, HashedPassword, FirstName, LastName)
            Values ('{}', '{}', '{}', '{}');
            '''.format(username, password, first_name, last_name))
        user_id = self.get_new_account_user_id(username)
        self.my_cursor.execute(
            '''
            UPDATE AppUser
            SET HomeUserId = '{}'
            WHERE username = '{}'
            '''.format(user_id, username)
        )

    def get_friends(self, username):
        user_id = self.get_user_id(username, username)
        self.my_cursor.execute('''
            Select U.UserName, U.UserId, U.FirstName, U.LastName
            From AppUser U
            Where U.HomeUserId = '{}' and U.UserId != '{}'
        '''.format(user_id, user_id))
        return self.my_cursor.fetchall()

    def get_individual_friend(self, home_username, friend_username):
        home_user_id = self.get_user_id(home_username, home_username)
        friend_user_id = self.get_user_id(home_username, friend_username)
        self.my_cursor.execute('''
            Select U.UserName, U.UserId, U.FirstName, U.LastName
            From AppUser U
            Where U.HomeUserId = '{}' and U.UserId = '{}'
        '''.format(home_user_id, friend_user_id))
        return self.my_cursor.fetchone()

    def get_individual_friend_by_id(self, home_username, friend_user_id):
        home_user_id = self.get_user_id(home_username, home_username)
        self.my_cursor.execute('''
                    Select U.UserName, U.UserId, U.FirstName, U.LastName
                    From AppUser U
                    Where U.HomeUserId = '{}' and U.UserId = '{}'
                '''.format(home_user_id, friend_user_id))
        return self.my_cursor.fetchone()

    def add_friend(self, username, first_name, last_name, home_username, hashed_pass):
        home_user_id = self.get_user_id(home_username, home_username)
        self.my_cursor.execute(
            '''
            INSERT INTO AppUser(UserName, HashedPassword, FirstName, LastName, HomeUserId)
            VALUES ('{}', '{}', '{}', '{}', '{}');
            '''.format(username, hashed_pass, first_name, last_name, home_user_id)
        )

    def delete_friend(self, home_username, friend_username):
        home_user_id = self.get_user_id(home_username, home_username)
        friend_user_id = self.get_user_id(home_username, friend_username)
        self.my_cursor.execute('''
            Delete From AppUser U 
            Where U.HomeUserId = '{}' and U.UserId = '{}'
        '''.format(home_user_id, friend_user_id)
        )

    def get_models_for_user(self, username):
        home_user_id = self.get_user_id(username, username)
        self.my_cursor.execute('''
        Select m.ModelId, m.FilePath
        From Model m
        Where m.UserId = '{}'
        '''.format(home_user_id))
        return self.my_cursor.fetchall()

    def get_all_classifications_for_model(self, model_id):
        self.my_cursor.execute('''
            Select C.ClassificationId, C.UserId, C.FirstName, C.LastName, C.Confidence, C.ClassificationTimestamp,
             C.ImagePath
            From ModelUserClassification C
            Where C.ModelId = '{}'
        '''.format(model_id))
        return self.my_cursor.fetchall()

    def save_model(self, home_user_id, filepath, model_name):
        self.my_cursor.execute('''
            INSERT INTO Model(UserId, FilePath, ModelName)
            VALUES ('{}', '{}', '{}');
        '''.format(home_user_id, filepath, model_name))

    def add_classification(self, model_id, is_train, classification):
        self.my_cursor.execute('''
            INSERT INTO ModelUserClassification(UserId, ModelId, FirstName, LastName, IsTrainClassification,
             ClassificationTimeStamp, ImagePath, Confidence)   
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')    
        '''.format(classification.user_id, model_id, classification.first_name, classification.last_name, is_train,
                   classification.timestamp, classification.image_path, classification.confidence))

    def get_active_model_id(self, home_user_id):
        self.my_cursor.execute('''
            Select M.ModelId
            From Model M
            Where M.IsActive = 1 and M.UserId = '{}'
        '''.format(home_user_id))
        return self.my_cursor.fetchone()[0]

    def get_active_model_name(self, home_user_id):
        self.my_cursor.execute('''
            Select M.ModelName
            From Model M
            Where M.IsActive = 1 and M.UserId = '{}'
        '''.format(home_user_id))
        return self.my_cursor.fetchone()[0]

    def set_model_active(self, user_id, model_id):
        self.my_cursor.execute('''
        Update Model M
        Set M.IsActive = 0
        Where M.IsActive = 1 and M.UserId = '{}';
        Update Model M
        Set M.IsActive = 1
        Where M.ModelId = '{}' and M.UserId = '{}'
        '''.format(user_id, model_id, user_id))

    def get_model_id_by_name(self, model_name):
        self.my_cursor.execute('''
            Select M.ModelId
            From Model M
            Where M.ModelName = '{}'
        '''.format(model_name))
        return self.my_cursor.fetchone()
