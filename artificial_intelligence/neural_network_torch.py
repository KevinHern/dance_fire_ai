import numpy as np
import timeit
from p5 import PI, TWO_PI, HALF_PI, QUARTER_PI
from torch.nn import Module, Linear
from torch.nn.functional import relu, sigmoid
from torch import from_numpy


class TorchNeuralNetwork(Module):
    def __init__(self, number_inputs, hidden_neurons, output_neurons):
        super(TorchNeuralNetwork, self).__init__()
        self.layer_1 = Linear(number_inputs, hidden_neurons)
        self.layer_2 = Linear(hidden_neurons, output_neurons)

    def forward(self, x):
        x = relu(self.layer_1(x))
        x = relu(self.layer_2(x))
        return x


# For training process: https://towardsdatascience.com/build-a-simple-neural-network-using-pytorch-38c55158028d

dummy = TorchNeuralNetwork(5, 4, 2)
dummy = dummy.double()

print(dummy)

inputs = np.array([PI, 0, 0, 1, 0])

print(dummy(from_numpy(inputs)))