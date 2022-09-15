# Basic imports
from p5 import *  # UI Stuff
import numpy as np
from random import randint

# AI Game imports
from dance_fire_ice.models.ai_agent_deep_q_learning import AgentQL
from dance_fire_ice.models.track import Track

# Track imports
from dance_fire_ice.utils.game_tracks import track_ai

# Optimization imports
from threading import Thread
from dance_fire_ice.utils.multi_threading import execute_agent_batch


### INITIALIZING CONSTANTS ###
# Screen constants
width = 1250
height = 800
frame_rate = 60

starting_x = width / 16
starting_y = height / 16

screen_speed = (0, 0)

# Track Variables
the_track = track_ai

# Agents variables
circles_diameter = 100
circles_radius = 40

bpm = 115

tile_size = circles_diameter / 2

max_episodes = 400
actions = 512

# Initializing Agents
q_agent = AgentQL(
        frame_rate=frame_rate,
        bpm=bpm,
        total_tiles=len(the_track),
        starting_x=starting_x,
        starting_y=starting_y,
        diameter=circles_diameter,
        circle_radius=circles_radius,
        actions=actions,
        max_episodes=max_episodes
    )

# Initializing Track
track = Track(
    pivot_x=starting_x,
    pivot_y=starting_y,
    tile_size=tile_size,
    track=the_track
)


# Setting up canvas and overall simulation
def setup():
    size(width, height)
    # no_loop()


# Repainting the canvas
def draw():
    global starting_x
    global starting_y

    # Clean Canvas
    background(0)

    # Draw the track for only one agent (the previous best one) to save up memory
    track.draw(tile_index=q_agent.next_tile)

    # Draw agent
    q_agent.agent.draw()

    # Perform action
    q_agent.perform_action(next_tile_direction=track.track[q_agent.next_tile])

    # Check if simulation has ended
    if q_agent.game_over:
        # Train agent
        q_agent.train()

        # Reset agent
        q_agent.reset_agent()

        # Reset track
        track.reset()


def mouse_pressed():
    redraw()


if __name__ == '__main__':
    run()


'''
    # TO DO
    - Optimize the draw() function by parallelize the perform_action with multi threading
    - Add screen info
    - Save best weights
'''