# Basic imports
from p5 import *  # UI Stuff
import numpy as np
from random import randint

# AI Game imports
from dance_fire_ice.models.ai_agent import AIAgent, crossover
from dance_fire_ice.models.track import Track

# Track imports
from dance_fire_ice.utils.game_tracks import track_ai

# Optimization imports
from threading import Thread
from dance_fire_ice.utils.multi_threading import execute_agent_batch


### INITIALIZING CONSTANTS ###
# Simulation constants
generation = 1
population = 500
max_lifespan = 500
lifespan = max_lifespan

agents_to_display = np.array([randint(0, population-1), randint(0, population-1), randint(0, population-1)])

mutation_probability = 0.10
min_alpha = 0.90
max_alpha = 1.10

# Optimization constants
number_threads = 5
agents_per_thread = population // number_threads
remaining_agents = population % number_threads
agents_thread_limit = []
for thread_id in range(number_threads):
    agents_thread_limit.append(agents_per_thread*thread_id)
agents_thread_limit.append(population)

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

    # MULTITHREADING
    # Create Threads
    threads = []
    for number_thread in range(number_threads):
        threads.append(
            Thread(
                target=execute_agent_batch,
                args=(agents[agents_thread_limit[number_thread]:agents_thread_limit[number_thread+1]], track)
            )
        )

    # Start threads
    for agent_thread in threads:
        agent_thread.start()

    # Perform best agent action
    best_agent.perform_action(next_tile_direction=track.track[best_agent.next_tile])

    # Wait for threads to finish
    for agent_thread in threads:
        agent_thread.join()

    # OLD SEQUENTIAL IMPLEMENTATION
    # for agent in agents:
    #     agent.perform_action(next_tile_direction=track.track[agent.next_tile])

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

        # Third: Select top 20%
        parents = agents[0:(population//5)]

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

        # Fifth: Reset simulation variables
        agents_to_display = np.array([randint(0, population-1), randint(0, population-1), randint(0, population-1)])
        lifespan = max_lifespan
        generation += 1
        print("Generation:", generation)

        # Reset best agent
        best_agent.reset(learn=False)

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