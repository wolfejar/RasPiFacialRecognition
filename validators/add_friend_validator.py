from models.sql import SQL
import random
import string
from passlib.hash import pbkdf2_sha256


def random_string(string_length=15):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def validate_friend(username, first_name, last_name, home_username):
    sql_instance = SQL()
    hashed_pass = pbkdf2_sha256.hash(random_string())
    try:
        sql_instance.add_friend(
            username=username, first_name=first_name, last_name=last_name, home_username=home_username,
            hashed_pass=hashed_pass
        )
        return True
    except():
        return False
