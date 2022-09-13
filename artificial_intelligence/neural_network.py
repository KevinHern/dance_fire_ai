import numpy as np
import timeit
from p5 import PI, TWO_PI, HALF_PI, QUARTER_PI


class NeuralNetwork:
    def __init__(self, number_inputs, hidden_neurons, output_neurons):
        # Initializing constants
        self.sigmoid = lambda x: 1 / (1 + np.exp(-x))
        self.relu = lambda x: max(0.0, x)

        # Initializing input layer
        self.input_weights = np.random.uniform(low=-1, high=1, size=(number_inputs, number_inputs))
        self.input_biases = np.random.uniform(low=-1, high=1, size=number_inputs)

        # Initializing hidden layer
        self.hidden_weights = np.random.uniform(low=-1, high=1, size=(number_inputs, hidden_neurons))
        self.hidden_biases = np.random.uniform(low=-1, high=1, size=hidden_neurons)

        # Initializing output layer
        self.output_weights = np.random.uniform(low=-1, high=1, size=(hidden_neurons, output_neurons))
        self.output_biases = np.random.uniform(low=-1, high=1, size=output_neurons)

    def forward_pass(self, inputs):
        # Forward propagation
        z = np.matmul(self.input_weights, inputs)
        z = z + self.input_biases

        z = np.array(list(map(self.relu, z)))

        z = np.matmul(z, self.hidden_weights)
        z = z + self.hidden_biases

        z = np.array(list(map(self.relu, z)))

        z = np.matmul(z, self.output_weights)
        z = z + self.output_biases

        z = np.array(list(map(self.relu, z)))

        return z


dummy = NeuralNetwork(
    number_inputs = 5, hidden_neurons = 4, output_neurons = 2
)

inputs = np.array([PI, 0, 0, 1, 0])

print(dummy.forward_pass(
    inputs=inputs
))

# print(timeit.timeit(lambda: dummy.forward_pass(
#     angle=30,
#     tile_up=0,
#     tile_down=0,
#     tile_left=1,
#     tile_right=0
# ), number=1))