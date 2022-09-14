import numpy as np
import timeit
from p5 import PI, TWO_PI, HALF_PI, QUARTER_PI
from torch.nn import Module, Linear, HuberLoss
from torch.nn.functional import relu, sigmoid
from torch import from_numpy
from torch.optim import SGD
from numpy import argmax


class TorchNeuralNetwork(Module):
    def __init__(self, number_inputs, hidden_neurons, output_neurons):
        super(TorchNeuralNetwork, self).__init__()
        self.layer_1 = Linear(number_inputs, hidden_neurons)
        self.layer_2 = Linear(hidden_neurons, output_neurons)

    def forward(self, x):
        x = relu(self.layer_1(x))
        x = relu(self.layer_2(x))
        return x


dummy_model = TorchNeuralNetwork(5, 4, 2).double()

inputs = np.array([PI, 0, 0, 1, 0])

result = dummy_model(from_numpy(inputs))
numpy_result = result.cpu().detach().numpy()

print(numpy_result[0], numpy_result[1], argmax(numpy_result))

# For training process: https://towardsdatascience.com/build-a-simple-neural-network-using-pytorch-38c55158028d

# Preparing dummy dataset
dummy_x = [[PI, 0, 0, 1, 0], [PI, 0, 0, 1, 0], [PI, 0, 0, 1, 0]]

dummy_x.append([PI, 0, 0, 1, 0])
dummy_x.append([PI, 0, 0, 1, 0])

data_x = from_numpy(np.array(dummy_x, dtype="float64"))

data_y = from_numpy(
    np.array([
        [10, 0.0],
        [15, 0.0],
        [2, 0.0],
        [5, 0.0],
        [10, 0.0],
    ])
).double()

print(data_x, data_y)

loss_function = HuberLoss()
optimizer = SGD(dummy_model.parameters(), lr=0.01)

for i in range(2):
    # Get predictions
    pred_y = dummy_model(data_x)

    # Calculate loss function
    loss = loss_function(pred_y, data_y)

    # Reset Grads
    dummy_model.zero_grad()

    # Back propagation
    loss.backward()
    optimizer.step()

result = dummy_model(from_numpy(inputs))
numpy_result = result.cpu().detach().numpy()

print(numpy_result[0], numpy_result[1], argmax(numpy_result))