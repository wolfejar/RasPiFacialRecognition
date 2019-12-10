from views.models_form import ModelsForm
from models.sql import SQL
from models.friend import Friend
from models.model_data import ModelData
from models.classification import Classification
import pandas as pd
import os


def build_model_form(username):
    sql_instance = SQL()
    results = sql_instance.get_friends(username=username)
    user_id = sql_instance.get_user_id(username, username)
    friends = []
    for friend in results:
        friends.append(Friend(username=friend[0], user_id=friend[1], first_name=friend[2], last_name=friend[3]))
    model_results = sql_instance.get_models_for_user(username=username)
    models = []
    for model in model_results:
        classification_results = sql_instance.get_all_classifications_for_model(model_id=model[0])
        classifications = []
        for c in classification_results:
            orig_path = c[6]
            print(orig_path)
            web_path = '../static/img/out/training/' + orig_path.split('/')[-2] + '/' + orig_path.split('/')[-1]
            classifications.append(Classification(c[1], c[2], c[3], c[4], c[5], web_path))
        models.append(ModelData(model_id=model[0], classifications=classifications, file_path=model[1]))
    x_vals, y_vals = get_training_data_distribution(username, sql_instance)
    return ModelsForm(user_id=user_id, friends=friends, models=models,
                      x_vals=x_vals, y_vals=y_vals)


def get_training_data_distribution(username, sql_instance):
    data_path = './static/img/out/training'
    friend_ids = [d for d in os.listdir(data_path) if not d.startswith('.')]
    counts = [[], []]
    for id in friend_ids:
        friend = sql_instance.get_individual_friend_by_id(username, id)
        # print(friend[2], friend[3], len(os.listdir(data_path + '/' + id)))
        counts[0].append(friend[2] + " " + friend[3])
        counts[1].append(len(os.listdir(data_path + '/' + id)))

    return counts
