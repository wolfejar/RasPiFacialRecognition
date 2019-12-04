from sql import SQL


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


def load_by_id(home_username, friend_id):
    sql_instance = SQL()
    result = sql_instance.get_individual_friend_by_id(home_username, friend_id)
    return Friend(username=result[0], user_id=result[1], first_name=result[2], last_name=result[3])


def load_all_friends(home_username):
    sql_instance = SQL()
    results = sql_instance.get_friends(username=home_username)
    friends = []
    for friend in results:
        friends.append(Friend(username=friend[0], user_id=friend[1], first_name=friend[2], last_name=friend[3]))
    return friends
