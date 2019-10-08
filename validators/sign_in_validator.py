from models.sql import SQL
from passlib.hash import pbkdf2_sha256


def validate_sign_in(username, password):
    sql_instance = SQL()
    hashed_pass = sql_instance.get_hashed_pass(username=username)
    if hashed_pass is None:
        return False
    else:
        return pbkdf2_sha256.verify(password, hashed_pass)
    return
