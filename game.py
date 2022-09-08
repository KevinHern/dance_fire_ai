import p5
from p5 import *
from beat_circles import BeatCircles
from track import Track
from constants import map_direction_to_track_speed
from game_tracks import track_one, track_dummy

# Initializing constants
width = 700
height = 500
starting_x = width / 2
starting_y = height / 2

circles_diameter = 100
circles_radius = 40

game_has_started = False
game_over = False

next_tile = 1

# Initializing Objects
beat_circles = BeatCircles(frame_rate=60,
                           bpm=115,
                           position_x=starting_x,
                           position_y=starting_y,
                           diameter=circles_diameter,
                           circle_radius=circles_radius
                           )

the_track = track_one

track = Track(
    pivot_x=starting_x,
    pivot_y=starting_y,
    tile_size=circles_diameter / 2,
    track=the_track
    # track=[
    #     TileDirection.INITIAL,
    #     TileDirection.RIGHT,
    #     TileDirection.RIGHT,
    #     TileDirection.RIGHT,
    #     TileDirection.DOWN,
    #     # TileDirection.RIGHT,
    #     # TileDirection.RIGHT,
    #     # TileDirection.RIGHT,
    #     # TileDirection.UP,
    #     # TileDirection.RIGHT,
    # ]
)

track_velocity_vector = list(
    map(
        lambda x:
        map_direction_to_track_speed(
            circles_linear_velocity=beat_circles.linear_velocity,
            tile_direction=x,
            alpha=3
        ),
        the_track
    )
)

# Initializing Vectors
screen_speed = (0, 0)


def setup():
    size(width, height)


def draw():
    global next_tile

    # Clean Canvas
    background(0)

    # Translating objects
    track.translate(speed=screen_speed)
    beat_circles.translate(speed=screen_speed)

    # Draw track
    # draw_track_tile(dummmy_tile)

    track.draw(tile_index=next_tile)

    # Draw circles
    beat_circles.draw()


def key_pressed():
    global game_has_started
    global game_over
    global screen_speed
    global track
    global next_tile

    if ord(str(key)) > 0:
        # Check game state
        if game_has_started:
            if beat_circles.change_anchor(tile_direction=track.track[next_tile]):
                screen_speed = track_velocity_vector[next_tile]
                next_tile += 1
                if next_tile >= len(track.track):
                    print("Track complete")
                    exit()
            else:
                print("Game Over")
                exit()
        else:
            # Changing game flag
            if beat_circles.change_anchor(tile_direction=track.track[next_tile]):
                screen_speed = track_velocity_vector[next_tile]
                next_tile += 1
                game_has_started = True
    else:
        pass


def mouse_pressed():
    redraw()


if __name__ == '__main__':
    run()
