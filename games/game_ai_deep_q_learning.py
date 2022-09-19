# Basic imports
from p5 import *  # UI Stuff
import numpy as np
from random import randint

# AI Game imports
from dance_fire_ice.models.ai_agent_deep_q_learning import AgentQL
from dance_fire_ice.models.track import Track

# Track imports
from dance_fire_ice.utils.game_tracks import track_ai1, track_ai2, track_ai3, track_ai4


### INITIALIZING CONSTANTS ###
# Screen constants
width = 1250
height = 800
frame_rate = 60

starting_x = width / 2
starting_y = height / 2

screen_speed = (0, 0)

# Track Variables
the_track = track_ai1

# Agents variables
circles_diameter = 100
circles_radius = 40

bpm = 115

tile_size = circles_diameter / 2

max_episodes = 400

# Train Batch
actions = 512

# Initializing Track
track = Track(
    pivot_x=starting_x,
    pivot_y=starting_y,
    tile_size=tile_size,
    track=the_track
)

# Shuffling tracks
tracks_training = [track_ai1, track_ai2, track_ai3, track_ai4]
current_track = 0
episodes_per_track = 10

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
        max_episodes=max_episodes,
        save_model_checkpoint=episodes_per_track,
    )

# Loading existing model
q_agent.load_model(episode=10)


# Setting up canvas and overall simulation
def setup():
    size(width, height)


# Repainting the canvas
def draw():
    global current_track
    global track

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

        # Shuffling track
        current_track += 1 if (q_agent.current_episode + 1) % episodes_per_track == 0 else 0
        current_track = current_track % len(tracks_training)
        track_to_train = tracks_training[current_track]

        # Initializing new track
        track = Track(
            pivot_x=starting_x,
            pivot_y=starting_y,
            tile_size=tile_size,
            track=track_to_train
        )

        # Reset agent
        q_agent.reset_agent()
        q_agent.total_tiles = len(track_to_train)


def mouse_pressed():
    redraw()


if __name__ == '__main__':
    run()


'''
    # TO DO
    - Shuffle between tracks so the AI can learn other movements and not get biased
    - Print stats every N episodes
'''