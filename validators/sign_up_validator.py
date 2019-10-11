from models.sql import SQL
from passlib.hash import pbkdf2_sha256


def validate_sign_up(username, password, first_name, last_name, role):
    sql_instance = SQL()
    hashed_pass = pbkdf2_sha256.hash(password)
    try:
        sql_instance.create_account(
            username=username, password=hashed_pass, first_name=first_name, last_name=last_name, role=role
        )
        return True
    except():
        return False
