import pickle
import os
import friend
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import itertools
import numpy as np


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


def train_classifier(user_id, friends, model_name, hidden_layers=[20], epochs=2000):
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
    x_train, x_test, y_train, y_test, indeces_train, indeces_test = train_test_split(x, y, indeces, test_size=0.3)
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
    optimizer = optim.SGD(itertools.chain(*params), lr=0.001, momentum=0.9)

    '''
    inp = torch.autograd.Variable(torch.randn(3, 5), requires_grad=True)
    target = torch.autograd.Variable(torch.LongTensor(3).random_(5))
    print(inp)
    print(target)
    '''
    for epoch in range(epochs):  # loop over the dataset multiple times

        running_loss = 0.0
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        # print(x_train)
        outputs = model(x_train)
        # print(outputs)
        # print(y_train)
        loss = criterion(outputs, y_train)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        print('%d loss: %.3f' % (epoch + 1, running_loss))
        # print('%d loss: %.3f out: %r' % (epoch + 1, running_loss, outputs))

    results = []
    for i, inp in enumerate(x_test):
        index = indeces_test[i]
        results.append((model(inp), y_test[i], index))
    out_path = os.path.abspath('./static/models/' + str(user_id))
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    torch.save(model, out_path + '/' + model_name + '.pt')

    print('Finished Training')

    return results


# train_classifier('1', [friend.load('wolfejar@ksu.edu', 'test@test.com')], 'test', hidden_layers=[30, 20, 10])
