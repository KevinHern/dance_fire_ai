# Basic imports
from p5 import *  # UI Stuff
import numpy as np
from random import randint

# AI Game imports
from ai_agent import AIAgent, crossover
from track import Track

# Track imports
from game_tracks import track_ai


### INITIALIZING CONSTANTS ###
# Simulation constants
generation = 1
population = 100
max_lifespan = 120
lifespan = max_lifespan

agents_to_display = np.array([randint(0, population-1), randint(0, population-1), randint(0, population-1)])

mutation_probability = 0.10
min_alpha = 0.90
max_alpha = 1.10

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

lives = 5

tile_size = circles_diameter / 2

# print(len(the_track))


# Initializing Agents
def create_agent():
    return AIAgent(
        frame_rate=frame_rate,
        bpm=bpm,
        total_tiles=len(the_track),
        starting_x=starting_x,
        starting_y=starting_y,
        diameter=circles_diameter,
        circle_radius=circles_radius,
        lives=lives
    )


agents = np.empty(population)
agents.fill(0)
agents = np.array(
    list(map(
        lambda x: create_agent(),
        agents
    )),
    dtype=AIAgent
)

# Initialize the best agent with the first specimen
best_agent = create_agent()

# print(agents)

# Initializing Track
track = Track(
    pivot_x=starting_x,
    pivot_y=starting_y,
    tile_size=circles_diameter / 2,
    track=the_track
)


# Setting up canvas and overall simulation
def setup():
    size(width, height)
    # no_loop()


# Repainting the canvas
def draw():
    global lifespan
    global agents
    global starting_x
    global starting_y
    global lives
    global lifespan
    global generation
    global best_agent
    global agents_to_display

    # Clean Canvas
    background(0)

    # Draw the track for only one agent (the previous best one) to save up memory
    track.draw(tile_index=best_agent.next_tile)

    # For each agent, perform the action
    for agent in agents:
        agent.perform_action(next_tile_direction=track.track[agent.next_tile])

    best_agent.perform_action(next_tile_direction=track.track[best_agent.next_tile])

    # Draw 3 random agents and the previous best agent on the screen
    best_agent.agent.draw()
    agents[agents_to_display[0]].agent.draw()
    agents[agents_to_display[1]].agent.draw()
    agents[agents_to_display[2]].agent.draw()

    # Check if simulation has ended
    if lifespan > 1:
        # Reduce timer
        lifespan -= 1
    else:
        ### BREEDING PROCESS ###
        # First: Sort by fitness
        agents = np.array(sorted(agents))

        # Second: Obtain best agent of the current generation and reset its tile count
        print(best_agent.fitness, agents[0].fitness)
        best_agent = agents[0] if agents[0].fitness > best_agent.fitness else best_agent
        best_agent.next_tile = 1
        #print(best_agent.fitness, agents[population-1].fitness)

        # Third: Select top 50%
        parents = agents[0:ceil(population/2)]

        # Fourth: Do crossover
        agents = np.array(
            list(map(
                lambda x: crossover(
                    parents=parents,
                    starting_x=starting_x,
                    starting_y=starting_y,
                    lives=lives,
                    bpm=frame_rate,
                    frame_rate=frame_rate,
                    mutation_probability=mutation_probability,
                    min_alpha=min_alpha,
                    max_alpha=max_alpha
                ),
                agents
            ))
        )

        # Fifth: Reset simulation and change the balls to draw
        agents_to_display = np.array([randint(0, population-1), randint(0, population-1), randint(0, population-1)])

        best_agent.reset(learn=False)

        lifespan = max_lifespan
        generation += 1
        print("Generation:", generation)


def mouse_pressed():
    redraw()


if __name__ == '__main__':
    run()


'''
    # TO DO
    - Optimize the draw() function by paralelizing the perform_action with multi threading
    - Penalize the AI for each full spin it does without doing nothing
    - Fix the 'action' button's direction
    - Add screen info
'''