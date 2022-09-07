import p5
from p5 import *
from beat_circles import BeatCircles
from track import Track, TrackTile, draw_track_tile, map_direction_to_offset
from constants import TileDirection
from game_tracks import track_one

# Initializing constants
width = 700
height = 500
starting_x = width / 2
starting_y = height / 2

circles_diameter = 100
circles_radius = 40

game_has_started = False
game_over = False

relation = (circles_radius * 0.35) / circles_diameter
horizontal_threshold = abs(tan(relation))
vertical_threshold = abs(tan(1 / relation))

next_tile = 1

# Initializing Objects
beat_circles = BeatCircles(frame_rate=60,
                           bpm=115,
                           position_x=starting_x,
                           position_y=starting_y,
                           diameter=circles_diameter,
                           circle_radius=circles_radius
                           )
track = Track(
    pivot_x=starting_x,
    pivot_y=starting_y,
    tile_size=circles_diameter / 2,
    track=track_one
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


def check_circles_angle():
    global beat_circles
    global next_tile

    # Calculate current TAN value
    current_tan = abs(tan(beat_circles.angle))

    if track.track[next_tile].value > 2:
        #print(horizontal_threshold, current_tan)
        return current_tan <= horizontal_threshold
    else:
        #print(vertical_threshold, current_tan)
        return current_tan >= vertical_threshold


def key_pressed():
    keyIndex = -1
    global game_has_started
    global game_over
    global screen_speed
    global track
    global next_tile

    if ord(str(key)) > 0:
        # Check game state
        if game_has_started:
            if check_circles_angle():
                beat_circles.change_anchor(tile_direction=track.track[next_tile])
                next_tile += 1
                if next_tile >= len(track.track):
                    exit()
            else:
                game_over = True
                exit()
        else:
            # Changing game flag
            if check_circles_angle():
                game_has_started = True
                beat_circles.change_anchor(tile_direction=track.track[next_tile])
                screen_speed = (-1, 0)
                next_tile += 1
    else:
        pass


def mouse_pressed():
    redraw()


if __name__ == '__main__':
    run()
