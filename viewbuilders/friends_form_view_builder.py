from models.sql import SQL
from views.friends_form import FriendsForm
from models.friend import Friend


def build_friends_form(username):
    sql_instance = SQL()
    results = sql_instance.get_friends(username=username)
    friends = []
    for friend in results:
        friends.append(Friend(username=friend[0], first_name=friend[1], last_name=friend[2]))
    return FriendsForm(friends=friends)
