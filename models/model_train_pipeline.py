import models.create_embeddings as ce
import models.train_model as tm
import os
from models.sql import SQL
import torch
from models.classification import Classification
from datetime import datetime
import pickle


def init_model_train_pipeline(home_id, friends, model_name, learning_rate=0.001, momentum=0.9, epochs=10000, split=0.2,
                              hidden_layers=[20]):
    ce.encode_faces(friends)
    test_results, metrics = tm.train_classifier(home_id, friends, model_name, hidden_layers=hidden_layers,
                                                learning_rate=learning_rate, epochs=epochs, momentum=momentum,
                                                split=split)
    # now that model is trained, we need to create objects to be stored in mysql
    # we need Model - modelid, userid, filepath
    # ModelClassifications - on test set we need to return the user_id, model_id, is_train (no), timestamp, image_path,
    # and confidence

    model_path = os.path.abspath('./static/models/' + str(home_id) + '/' + model_name + '.pt')
    model = torch.load(model_path)
    model.eval()
    model_name = model_path.split('/')[-1][:-3]

    sql_instance = SQL()
    sql_instance.save_model(home_id, model_path, model_name)
    print(model_name)
    model_id = sql_instance.get_model_id_by_name(model_name)
    print(model_id)
    metrics.model_id = model_id
    cls = []
    for result in test_results:
        r = []
        train_img_index = result[2]
        result = result[0].tolist()
        r.append((result.index(max(result)), max(result), train_img_index))
        cls.append(r)

    print(cls)
    classifications = []
    image_paths = []
    for f in friends:
        current_dir = os.path.abspath('./static/img/out/training/' + str(f.user_id) + '/')
        for img in os.listdir(current_dir):
            image_paths.append(current_dir + '/' + img)
    # for i, path in enumerate(image_paths):
    #    print(i, path.split('/')[-2:])
    for i, c in enumerate(cls):
        classifications.append(Classification(friends[c[0][0]].user_id, friends[c[0][0]].first_name,
                                              friends[c[0][0]].last_name, c[0][1], datetime.now(),
                                              image_paths[c[0][2]]))

    for c in classifications:
        print(c.user_id)
        sql_instance.add_classification(model_id, 1, c)

    metrics_path = os.path.abspath('./static/models/metrics/' + str(home_id) + '/')
    if not os.path.exists(metrics_path):
        os.mkdir(metrics_path)
    f = open(metrics_path + '/' + str(model_id) + '.pickle', "wb+")
    f.write(pickle.dumps(metrics))
    f.close()


def set_active(user_id, model_id):
    sql_instance = SQL()
    sql_instance.set_model_active(user_id, model_id)


def get_active_id(user_id):
    sql_instance = SQL()
    return int(sql_instance.get_active_model_id(user_id))


def get_active_name(user_id):
    sql_instance = SQL()
    return sql_instance.get_active_model_name(user_id)
