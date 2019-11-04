from models.sql import SQL
import models.friend
import os
import shutil


def validate_delete_friend(home_username, friend_username):
    sql_instance = SQL()
    friend = models.friend.load(home_username, friend_username)
    data_folder = os.path.abspath('./static/img/data/' + str(friend.user_id) + '/')
    training_folder = os.path.abspath('./static/img/out/training/' + str(friend.user_id) + '/')
    shutil.rmtree(data_folder)
    shutil.rmtree(training_folder)
    sql_instance.delete_friend(home_username, friend_username)
