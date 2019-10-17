from sql import SQL


def validate_friend(username, first_name, last_name, home_username):
    sql_instance = SQL()
    try:
        sql_instance.add_friend(
            username=username, first_name=first_name, last_name=last_name, home_username=home_username
        )
        return True
    except():
        return False
