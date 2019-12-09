import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import itertools
import numpy as np
from torchviz import make_dot
from models.model_metrics import ModelMetrics


class MyNet(nn.Module):

    def __init__(self, layers):
        super(MyNet, self).__init__()
        self.layers = []
        for i in range(0, len(layers)-1):
            self.layers.append(nn.Linear(layers[i], layers[i+1]))

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            if i < len(self.layers) - 1:
                x = F.relu(layer(x))
            else:
                x = layer(x)
        return x


def train_classifier(user_id, friends, model_name, learning_rate=0.001, momentum=0.9, split=0.2, hidden_layers=[20],
                     epochs=10000):
    friend_data = []
    corresponding_training_photos = []
    input_path = os.path.abspath('./static/img/out/embeddings/')
    for fr in friends:
        embeddings_dir = os.path.abspath(input_path + '/' + str(fr.user_id) + '/')
        embeddings_paths = os.listdir(embeddings_dir)
        fr_training_photos = os.path.abspath('./static/img/out/training/' + str(fr.user_id) + '/')
        training_photos_paths = os.listdir(fr_training_photos)
        for path in training_photos_paths:
            corresponding_training_photos.append(fr_training_photos + '/' + path)
        for path in embeddings_paths:
            data = pickle.loads(open(embeddings_dir + '/' + path, "rb").read())
            friend_data.append(data)

    all_classes = [data['user_id'] for data in friend_data]
    all_names = [f.first_name + ' ' + f.last_name for f in friends]
    labels = []
    cur_class = all_classes[0]
    cur_label = 0
    for cl in all_classes:
        if cl != cur_class:
            cur_class = cl
            cur_label += 1
        labels.append(cur_label)
    for i, label in enumerate(labels):
        new = [0] * len(friends)
        print(label)
        new[label] = 1
        labels[i] = new
    print(labels)
    x = np.array([data['encodings'][0] for data in friend_data])
    y = np.array([label for label in labels])
    indeces = range(len(y))
    x_train, x_test, y_train, y_test, indeces_train, indeces_test = train_test_split(x, y, indeces, test_size=split)
    print(len(x_train), len(y_train), len(x_test), len(y_test))
    print(indeces_train, indeces_test)
    x_train = torch.from_numpy(x_train).float()
    y_train = torch.from_numpy(y_train).float()
    x_test = torch.from_numpy(x_test).float()
    y_test = torch.from_numpy(y_test).float()

    print(x_train)
    print(y_train)

    layers = [128]  # input
    for layer in hidden_layers:
        layers.append(layer)  # hidden
    layers.append(len(friends))  # output
    print(layers)

    model = MyNet(layers)

    criterion = nn.MSELoss()
    params = [layer.parameters() for layer in model.layers]
    optimizer = optim.SGD(itertools.chain(*params), lr=learning_rate, momentum=momentum)

    acc = 0
    epoch = 0
    lowest_loss = 2
    loss = 0
    loss_data = []
    # for epoch in range(epochs):  # loop over the dataset multiple times
    while (acc < 1 or epoch < epochs) and epoch < 30000:
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = model(x_train)
        out_test = model(x_test)
        loss = criterion(outputs, y_train)
        loss_data.append(loss)
        loss.backward()
        optimizer.step()
        acc = accuracy_score(np.argmax(y_test.tolist(), axis=1), np.argmax(out_test.tolist(), axis=1))
        print('%d loss: %.3f acc: %.3f' % (epoch + 1, loss.item(), acc))
        epoch += 1
        if loss < lowest_loss:
            lowest_loss = loss
        # print('%d loss: %.3f out: %r' % (epoch + 1, loss.item(), outputs))

    results = []
    y_pred = []
    for i, inp in enumerate(x_test):
        index = indeces_test[i]
        out = model(inp)
        y_pred.append(out.tolist())
        results.append((out, y_test[i], index))
    out_path = os.path.abspath('./static/models/' + str(user_id))
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    torch.save(model, out_path + '/' + model_name + '.pt')

    print('Finished Training')
    print(np.argmax(y_pred, axis=1), np.argmax(y_test.tolist(), axis=1))
    print('Accuracy:', accuracy_score(np.argmax(y_test.tolist(), axis=1), np.argmax(y_pred, axis=1)))
    dot = make_dot(model(x_test[0]), params=None)
    graph_path = os.path.abspath('./static/img/model_graphs/' + str(user_id))
    if not os.path.exists(graph_path):
        os.mkdir(graph_path)
    dot.render(filename=model_name, directory=graph_path, format='png')
    metrics = ModelMetrics(model_id=None, y_pred=[all_names[i] for i in np.argmax(y_pred, axis=1)],
                           y_true=[all_names[i] for i in np.argmax(y_test.tolist(), axis=1)],
                           labels=all_names, loss_data=[d.item() for d in loss_data])

    return results, metrics


def softmax_numpy(scores):
    return np.exp(scores)/sum(np.exp(scores))
