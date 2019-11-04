from models.sql import SQL
import models.friend
import os


def validate_delete_friend(home_username, friend_username):
    sql_instance = SQL()

    friend = models.friend.load(home_username, friend_username)
    data_folder = os.path.abspath('./static/img/data/' + str(friend.user_id) + '/')
    training_folder = os.path.abspath('./static/img/out/training/' + str(friend.user_id) + '/')
    for the_file in os.listdir(data_folder):
        file_path = os.path.join(data_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    for the_file in os.listdir(training_folder):
        file_path = os.path.join(training_folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

    sql_instance.delete_friend(home_username, friend_username)
