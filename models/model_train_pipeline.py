import models.create_embeddings as ce
import models.train_model as tm
import os
from models.sql import SQL
from train_model import MyNet
import torch
from models.classification import Classification
from datetime import datetime
from imutils import paths


def init_model_train_pipeline(home_id, friends, model_name):
    ce.encode_faces(friends)
    test_results = tm.train_classifier(home_id, friends, model_name)
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
    model_id = sql_instance.get_model_id_by_name(model_name)[0]
    print(model_id)
    classi_bois = []
    for result in test_results:
        butt = []
        print(result[0])
        train_img_index = result[2]
        result = result[0]
        butt.append((result.tolist().index(max(result.tolist())), max(result.tolist()), train_img_index-1))
        print(butt)
        classi_bois.append(butt)

    print(classi_bois)
    classifications = []
    image_paths = []
    for f in friends:
        current_dir = os.path.abspath('./static/img/out/training/' + str(f.user_id) + '/')
        for img in paths.list_images(current_dir):
            image_paths.append(current_dir + '/' + img)
    print(image_paths)
    for i, c in enumerate(classi_bois):
        classifications.append(Classification(friends[c[0][0]].user_id, friends[c[0][0]].first_name,
                                              friends[c[0][0]].last_name, c[0][1], datetime.now(),
                                              image_paths[c[0][2]]))

    print(classifications)
    for c in classifications:
        print(c.user_id)
        sql_instance.add_classification(model_id, 1, c)



