from models.sql import SQL


class Friend:
    def __init__(self, username, user_id, first_name, last_name):
        self.username = username
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name


def load(home_username, friend_username):
    sql_instance = SQL()
    result = sql_instance.get_individual_friend(home_username, friend_username)
    return Friend(username=result[0], user_id=result[1], first_name=result[2], last_name=result[3])
