# Agent implemented with Deep Q Learning
# https://www.analyticsvidhya.com/blog/2019/04/introduction-deep-q-learning-python/

# Models
import math

from dance_fire_ice.models.ai_agent import AIAgent
from dance_fire_ice.artificial_intelligence.neural_network_torch import TorchNeuralNetwork

# AI Libraries
from torch import from_numpy
from torch.nn import HuberLoss
from torch.optim import SGD
from torch import save, load

# Utils
import numpy as np
from random import randint, random
from os import getcwd
from os.path import join, split
from math import ceil
import logging


def get_q_model_directory(model_name):
    # Get models directory
    directory_name = "deep_q_models"

    # Creating path
    cwd = getcwd()
    split_path = list(split(cwd))
    split_path[-1] = directory_name
    split_path.append(model_name)

    model_path = join(split_path[0])
    for i in range(len(split_path)):
        model_path = join(model_path, split_path[i])

    return model_path


class AgentQL(AIAgent):
    REWARD = 100
    PUNISHMENT = 0

    SUCCESSFUL_ANCHOR_REWARD = [REWARD, PUNISHMENT]
    FAILED_ANCHOR_REWARD = [PUNISHMENT, REWARD]
    SUCCESSFUL_WAIT = FAILED_ANCHOR_REWARD
    FAILED_WAIT = SUCCESSFUL_ANCHOR_REWARD

    def __init__(
            self,
            # Original Parameters
            frame_rate,
            bpm,
            starting_x,
            starting_y,
            total_tiles,
            diameter=10,
            circle_radius=20,

            # Q Learning Parameters
            actions=10,
            trainable=True,
            number_tiles_checkpoint=5,
            max_episodes=100,
            alpha=0.93,
            save_model_checkpoint=5,
    ):
        # Initializing parent class's
        super(AgentQL, self).__init__(
            frame_rate=frame_rate,
            bpm=bpm,
            starting_x=starting_x,
            starting_y=starting_y,
            total_tiles=total_tiles,
            diameter=diameter,
            circle_radius=circle_radius,
            lives=actions,
            trainable=trainable
        )

        # Defining AI
        self.brain = TorchNeuralNetwork(
            number_inputs=5,
            hidden_neurons=4,
            output_neurons=2
        ).double()
        self.loss_function = HuberLoss()
        self.optimizer = SGD(self.brain.parameters(), lr=0.01)

        # Defining Q Learning Variables
        self.number_actions = 2

        self.current_episode = 1
        self.trainable_episodes = ceil(max_episodes*0.90)
        self.max_episodes = max_episodes

        self.alpha = alpha

        self.exploration_rate = 1.0
        self.exploration_decay = self.exploration_rate/self.trainable_episodes

        self.inputs_batch = []
        self.rewards_batch = []

        # Additional Q variables
        self.number_tiles_checkpoint = number_tiles_checkpoint
        self.checkpoint_next_tile = self.next_tile

        self.save_model_checkpoint = save_model_checkpoint

        # Stats variables
        self.random_actions_counter = 0
        self.brain_actions_counter = 0

        # Initializing logger
        logging.basicConfig(
            filename='training_log_q_learning.log',
            filemode='w',
            level=logging.INFO,
            format='\n%(asctime)s-%(levelname)s> %(message)s',
            datefmt='%d-%b-%y %H:%M:%S'
        )

    def take_action(self, inputs):
        if self.trainable and (self.exploration_rate > random()):
            # Take one random action when exploring
            self.random_actions_counter += 1

            return randint(0, self.number_actions - 1)
        else:
            # Forward pass
            self.brain_actions_counter += 1

            result = self.brain(from_numpy(inputs))
            numpy_result = result.cpu().detach().numpy()

            return np.argmax(numpy_result)

    def perform_action(self, next_tile_direction):
        if not self.game_over:
            # Prepare inputs
            inputs = np.empty(5)
            inputs.fill(0)

            inputs[0] = self.agent.angle
            inputs[next_tile_direction.value] = 1

            # Append inputs
            self.inputs_batch.append(inputs)

            # AI performs an action
            action = self.take_action(inputs=inputs)

            # Perform action of the agent
            if action == 0:
                # The agent tries to anchor new center to a new position
                if self.agent.change_anchor(tile_direction=next_tile_direction):
                    # The agent managed to successfully change tiles and moves on to the next tile
                    self.next_tile += 1

                    # Determine game over
                    self.game_over = self.next_tile == self.total_tiles
                    if self.game_over:
                        self.next_tile -= 1

                    # Reward for successful anchoring
                    self.rewards_batch.append(AgentQL.SUCCESSFUL_ANCHOR_REWARD)

                else:
                    # Reduce number of lives
                    self.lives -= 1

                    # Punish for not properly waiting
                    self.rewards_batch.append(AgentQL.FAILED_WAIT)
            else:
                # Check if the agent could anchor
                if self.agent.check_circles_angle(next_tile=next_tile_direction):
                    # Reduce number of lives
                    self.lives -= 1

                    # Punish for failed anchoring
                    self.rewards_batch.append(AgentQL.FAILED_ANCHOR_REWARD)
                else:
                    # Reward for waiting successfully
                    self.rewards_batch.append(AgentQL.SUCCESSFUL_WAIT)

            # Determine Game Over
            self.game_over = self.lives == 0

    def train(self):
        # Train model
        if self.trainable:
            # Preparing inputs to train
            train_batch = from_numpy(np.array(self.inputs_batch, dtype="float64"))
            output_batch = from_numpy(np.array(self.rewards_batch, dtype="float64"))

            # Getting current network's thoughts
            prediction_batch = self.brain(train_batch)

            # Calculating loss
            loss = self.loss_function(prediction_batch, output_batch)

            # Reset Grads
            self.brain.zero_grad()

            # Back propagation
            loss.backward()
            self.optimizer.step()

            # Reduce exploration rate
            self.exploration_rate -= self.exploration_decay if self.exploration_rate > 0 else 0

        # Save model
        if self.current_episode % self.save_model_checkpoint == 0:
            self.save_model()

    def log_stats(self):
        message = "\n---END OF EPISODE {}---\n".format(self.current_episode)
        message += "Current Exploration Probability: {:.2f}%\n".format(self.exploration_rate * 100)
        message += "Reached Tile number {} out of {}\n".format(self.next_tile - 1, self.total_tiles)
        message += "Track {:.2f}% completed\n".format(100*(self.next_tile - 1)/self.total_tiles)
        message += "Total Mistakes (lives) committed: {}\n".format(self.max_lives - self.lives + 1)
        message += "Total Random Actions Taken: {}\n".format(self.random_actions_counter)
        message += "Total Brain Actions Taken: {}".format(self.brain_actions_counter)

        # Logging
        logging.info(
            msg=message
        )

    def reset_agent(self):
        # Print stats
        self.log_stats()

        # Resetting agent
        self.reset(trainable=self.current_episode < self.trainable_episodes)

        # Resetting Q Variables
        self.current_episode += 1

        self.inputs_batch.clear()
        self.rewards_batch.clear()

        # Resetting Stats Variables
        self.random_actions_counter = 0
        self.brain_actions_counter = 0

    def save_model(self):
        # Naming model
        model_name = "dql_model_ep_" + str(self.current_episode) + ".pt"

        model_path = get_q_model_directory(model_name=model_name)

        # Saving model
        save(self.brain, model_path)

    def load_model(self, episode):
        # Naming model
        model_name = "dql_model_ep_" + str(episode) + ".pt"

        model_path = get_q_model_directory(model_name=model_name)

        # Loading model
        self.brain = load(model_path)
        self.brain.train()


