import torch
import torch.nn.functional as F
import os
import numpy as np
from models.sql import SQL


class EmbeddingsClassifier:
    def __init__(self, home_id, model_name):
        self.model_path = os.path.abspath('./static/models/' + str(home_id) + '/' + model_name + '.pt')
        model = torch.load(self.model_path)
        model.eval()
        self.model = model
        self.model_name = model_name
        sql_instance = SQL()
        self.model_id = sql_instance.get_model_id_by_name(model_name)

    def classify_embeddings(self, embeddings):
        embeddings = torch.from_numpy(np.array(embeddings)).float()
        return self.model(embeddings)
