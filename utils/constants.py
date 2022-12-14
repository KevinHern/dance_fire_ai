from enum import Enum
from p5 import PI, HALF_PI


def map_direction_to_track_speed(circles_linear_velocity, tile_direction, alpha=2.5):
    velocity = [0, 0]
    if tile_direction == TileDirection.UP:
        velocity[1] = circles_linear_velocity/alpha
    elif tile_direction == TileDirection.DOWN:
        velocity[1] = -circles_linear_velocity/alpha
    elif tile_direction == TileDirection.RIGHT:
        velocity[0] = -circles_linear_velocity/alpha
    elif tile_direction == TileDirection.LEFT:
        velocity[0] = circles_linear_velocity/alpha
    else:
        pass

    return velocity


def map_direction_to_vertical_unitary(tile_direction):
    if tile_direction == TileDirection.UP:
        return -1
    elif tile_direction == TileDirection.DOWN:
        return 1
    else:
        return 0


def map_direction_to_horizontal_unitary(tile_direction):
    if tile_direction == TileDirection.RIGHT:
        return 1
    elif tile_direction == TileDirection.LEFT:
        return -1
    else:
        return 0


def map_direction_to_offset(tile_direction):
    if tile_direction == TileDirection.RIGHT:
        return 0
    elif tile_direction == TileDirection.LEFT:
        return PI
    elif tile_direction == TileDirection.UP:
        return -HALF_PI
    else:
        return HALF_PI


class TileDirection(Enum):
    INITIAL = 0
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class TrackChunkType(Enum):
    TRANSITION = 1
    NORMAL = 2
    CACHED = 3
