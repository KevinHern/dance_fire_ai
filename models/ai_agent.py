from dance_fire_ice.models.beat_circles import BeatCircles
import numpy as np
from random import randint, choice, random, uniform


def get_random_agent(population):
    return randint(0, population-1)


class AIAgent:
    REWARD = 15
    PENALIZATION = 20

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
        # Creating Agent
        self.agent = BeatCircles(
            frame_rate=frame_rate,
            bpm=bpm,
            starting_x=starting_x,
            starting_y=starting_y,
            diameter=diameter,
            circle_radius=circle_radius
        )

        # Global Game state
        self.total_tiles = total_tiles

        # Defining Simulation Variables
        self.max_lives = lives
        self.lives = lives
        self.next_tile = 1

        # Settings flags
        self.game_over = False
        self.learn = learn

    def reset(self, learn=False):
        # Resetting agents variables
        self.lives = self.max_lives
        self.next_tile = 1

        # Resetting Flags
        self.game_over = False
        self.learn = learn

        # Resetting Agent
        self.agent.reset()
