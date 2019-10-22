from imutils import paths
from models.sql import SQL
from views.edit_friend_form import EditFriendForm
from models.friend import Friend
import os


def build_edit_friend_form(home_username, friend_username):
    sql_instance = SQL()
    result = sql_instance.get_individual_friend(home_username=home_username, friend_username=friend_username)
    print(result)
    friend = Friend(username=result[0], first_name=result[1], last_name=result[2])
    friend_path = os.path.abspath('static/img/data/' + friend_username)
    print(friend_path)
    image_paths = list(paths.list_images(friend_path))
    web_img_paths = []
    for image_path in image_paths:
        file_name = image_path.split('/')[-1]
        web_path = '../static/img/data/' + friend_username + '/' + file_name
        web_img_paths.append(web_path)
    print(web_img_paths)
    return EditFriendForm(friend=friend, image_paths=web_img_paths)
