from imutils import paths
from models.sql import SQL
from views.edit_friend_form import EditFriendForm
from models.friend import Friend
import os


def build_edit_friend_form(home_username, friend_username, review):
    sql_instance = SQL()
    result = sql_instance.get_individual_friend(home_username=home_username, friend_username=friend_username)
    print(result)
    friend = Friend(username=result[0], user_id=result[1], first_name=result[2], last_name=result[3])
    web_img_paths = []
    if review:
        friend_path = os.path.abspath('static/img/out/needs_review/')
        print(friend_path)
        image_paths = list(paths.list_images(friend_path))
        for image_path in image_paths:
            file_name = image_path.split('/')[-1]
            web_path = '../static/img/out/needs_review/' + file_name
            web_img_paths.append(web_path)
        print(web_img_paths)
    else:
        friend_path = os.path.abspath('static/img/data/' + str(friend.user_id))
        print(friend_path)
        image_paths = list(paths.list_images(friend_path))
        for image_path in image_paths:
            file_name = image_path.split('/')[-1]
            web_path = '../static/img/data/' + str(friend.user_id) + '/' + file_name
            web_img_paths.append(web_path)
        print(web_img_paths)
    return EditFriendForm(friend=friend, image_paths=web_img_paths)
