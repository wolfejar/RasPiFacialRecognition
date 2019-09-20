import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data.sampler import SubsetRandomSampler
from torch.autograd import Variable
import torch.nn.functional as F

seed = 42
np.random.seed(seed)
torch.manual_seed(seed)

# The compose function allows for multiple transforms
# transforms.ToTensor() converts our PILImage to a tensor of shape (C x H x W) in the range [0,1]
# transforms.Normalize(mean,std) normalizes a tensor to a (mean, std) for (R, G, B)
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

train_set = torchvision.datasets.CIFAR10(root='./cifardata', train=True, download=True, transform=transform)

test_set = torchvision.datasets.CIFAR10(root='./cifardata', train=False, download=True, transform=transform)

classes = ('plane', 'car', 'bird', 'cat',
           'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# Training
n_training_samples = 20000
train_sampler = SubsetRandomSampler(np.arange(n_training_samples, dtype=np.int64))

# Validation
n_val_samples = 5000
val_sampler = SubsetRandomSampler(np.arange(n_training_samples, n_training_samples + n_val_samples, dtype=np.int64))

# Test
n_test_samples = 5000
test_sampler = SubsetRandomSampler(np.arange(n_test_samples, dtype=np.int64))


class SimpleCNN(torch.nn.Module):

    # Our batch shape for input x is (3, 32, 32)

    def __init__(self):
        super(SimpleCNN, self).__init__()

        # Input channels = 3, output channels = 18
        self.conv1 = torch.nn.Conv2d(3, 18, kernel_size=3, stride=1, padding=1)
        self.pool = torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0)

        # 4608 input features, 64 output features (see sizing flow below)
        self.fc1 = torch.nn.Linear(18 * 16 * 16, 64)

        # 64 input features, 10 output features for our 10 defined classes
        self.fc2 = torch.nn.Linear(64, 10)

    def forward(self, x):
        # Computes the activation of the first convolution
        # Size changes from (3, 32, 32) to (18, 32, 32)
        x = F.relu(self.conv1(x))

        # Size changes from (18, 32, 32) to (18, 16, 16)
        x = self.pool(x)

        # Reshape data to input to the input layer of the neural net
        # Size changes from (18, 16, 16) to (1, 4608)
        # Recall that the -1 infers this dimension from the other given dimension
        x = x.view(-1, 18 * 16 * 16)

        # Computes the activation of the first fully connected layer
        # Size changes from (1, 4608) to (1, 64)
        x = F.relu(self.fc1(x))

        # Computes the second fully connected layer (activation applied later)
        # Size changes from (1, 64) to (1, 10)
        x = self.fc2(x)
        return x


def output_size(in_size, kernel_size, stride, padding):
    output = int((in_size - kernel_size + 2*padding) / stride) + 1
    return output


def get_most_recent_model():
    return


def train_model():
    return


def select_model_by_id():
    return
