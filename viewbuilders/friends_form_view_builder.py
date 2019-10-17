from models.sql import SQL
from friends_form import FriendsForm


def build_friends_form(username):
    sql_instance = SQL()
    friends = sql_instance.get_friends(username=username)
    return FriendsForm(friends=friends)
