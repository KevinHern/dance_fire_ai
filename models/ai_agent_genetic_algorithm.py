from dance_fire_ice.models.ai_agent import AIAgent
from dance_fire_ice.models.beat_circles import BeatCircles
from dance_fire_ice.artificial_intelligence.neural_network import NeuralNetwork
import numpy as np
from random import randint, choice, random, uniform


def sort_agents_by_fitness(agents):
    agents.sort(key=lambda x: x.fitness)


def crossover(
        parents,
        starting_x, starting_y,
        lives, bpm, frame_rate,
        mutation_probability=0.10, min_alpha=0.90, max_alpha=1.10
    ):

    # First: Selecting parents
    parent_a = parents[randint(0, parents.size-1)]
    parent_b = parents[randint(0, parents.size-1)]

    # Second: Create child
    offspring = AgentGA(
        frame_rate=frame_rate,
        bpm=bpm,
        starting_x=starting_x,
        starting_y=starting_y,
        diameter=parent_a.agent.radius*2,
        circle_radius=parent_a.agent.circle_radius,
        lives=lives,
        total_tiles=parent_a.total_tiles
    )

    # Third determine what genes are passed over
    boolean_dice = choice([True, False])

    if boolean_dice:
        # Parent A passes down Input Weights+Biases
        offspring.brain.input_weights = parent_a.brain.input_weights
        offspring.brain.input_biases = parent_a.brain.input_biases

        # Parent B passes down Hidden layer and Output Weights+Biases
        offspring.brain.hidden_weights = parent_b.brain.hidden_weights
        offspring.brain.hidden_biases = parent_b.brain.hidden_biases

        offspring.brain.output_weights = parent_b.brain.output_weights
        offspring.brain.output_biases = parent_b.brain.output_biases
        pass
    else:
        # Parent A passes down Hidden layer and Output Weights+Biases
        offspring.brain.input_weights = parent_b.brain.input_weights
        offspring.brain.input_biases = parent_b.brain.input_biases

        # Parent B passes down Input Weights+Biases
        offspring.brain.hidden_weights = parent_a.brain.hidden_weights
        offspring.brain.hidden_biases = parent_a.brain.hidden_biases

        offspring.brain.output_weights = parent_a.brain.output_weights
        offspring.brain.output_biases = parent_a.brain.output_biases
        pass

    # Mutate
    if random() < mutation_probability:
        # Mutating weights and biases
        # Multiply all of them by a random number between (min_alpha, max_alpha)
        offspring.brain.input_weights = offspring.brain.input_weights * uniform(min_alpha, max_alpha)
        offspring.brain.input_biases = offspring.brain.input_biases * uniform(min_alpha, max_alpha)

        offspring.brain.hidden_weights = offspring.brain.hidden_weights * uniform(min_alpha, max_alpha)
        offspring.brain.hidden_biases = offspring.brain.hidden_biases * uniform(min_alpha, max_alpha)

        offspring.brain.output_weights = offspring.brain.output_weights * uniform(min_alpha, max_alpha)
        offspring.brain.output_biases = offspring.brain.output_biases * uniform(min_alpha, max_alpha)
    else:
        pass

    # Return child
    return offspring


class AgentGA(AIAgent):
    def __init__(
            self,
            frame_rate,
            bpm,
            starting_x,
            starting_y,
            total_tiles,
            diameter=10,
            circle_radius=20,
            lives=5,
            learn=True
    ):
        # Initializing parent class's
        super(AgentGA, self).__init__(
            frame_rate=frame_rate,
            bpm=bpm,
            starting_x=starting_x,
            starting_y=starting_y,
            total_tiles=total_tiles,
            diameter=diameter,
            circle_radius=circle_radius,
            lives=lives,
            learn=learn
        )

        # Defining AI
        self.brain = NeuralNetwork(
            number_inputs=5,
            hidden_neurons=4,
            output_neurons=2
        )

        # Defining Generative Variables
        self.fitness = 0

    def __eq__(self, other):
        return self.fitness == other.fitness and self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness > other.fitness

    def perform_action(self, next_tile_direction):
        if not self.game_over:
            # Prepare inputs
            inputs = np.empty(5)
            inputs.fill(0)

            inputs[0] = self.agent.angle
            inputs[next_tile_direction.value] = 1

            # Forward pass
            result = self.brain.forward_pass(inputs=inputs)

            # The expected result of the AI is a number between [0, 1]
            if np.argmax(result) == 0:
                # Perform action of the agent
                if self.agent.change_anchor(tile_direction=next_tile_direction):
                    # The agent managed to successfully change tiles
                    # Increasing fitness for each tile
                    self.fitness += AIAgent.REWARD if self.learn else 0

                    # Move on to the next tile
                    self.next_tile += 1

                    # Determine game over
                    self.game_over = self.next_tile == self.total_tiles

                    if self.game_over:
                        self.next_tile -= 1

                else:
                    # Penalize the AI and reduce the number of lives until it is game over
                    self.lives -= 1
                    self.fitness -= AIAgent.PENALIZATION if self.learn else 0

                    # Determine game over
                    self.game_over = self.lives == 0
            else:
                # Do nothing
                pass
