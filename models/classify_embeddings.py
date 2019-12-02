import torch
import os
import numpy as np


class EmbeddingsClassifier:
    def __init__(self, home_id, model_name):
        self.model_path = os.path.abspath('./static/models/' + str(home_id) + '/' + model_name + '.pt')
        model = torch.load(self.model_path)
        model.eval()
        self.model = model
        self.model_name = self.model_path.split('/')[-1][:-3]

    def classify_embeddings(self, embeddings):
        embeddings = torch.from_numpy(np.array(embeddings)).float()
        return self.model(embeddings)
