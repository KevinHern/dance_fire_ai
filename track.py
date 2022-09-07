from p5 import *
from constants import *
import numpy as np


def draw_track_tile(tile):
    # Translate to the corresponding tile corner
    translate(tile.corner_x, tile.corner_y)

    # Draw tile
    rect((0, 0), tile.tile_size, tile.tile_size)


class Track:
    def __init__(self, pivot_x, pivot_y, tile_size, track):
        # Initializing track
        self.track = track
        self.tile_size = tile_size

        # Initializing track centers
        self.pivot_normal = (pivot_x, pivot_y)
        self.pivot_transition = (pivot_x, pivot_y)

        # Initializing constants
        self.chunk = 0
        self.normal_track_size = 4
        self.transition_track_size = 4
        self.chunk_size = self.normal_track_size + self.transition_track_size

        # Initializing tracks
        self.cached_track_chunk = []

        self.normal_track = []
        self.normal_track_directions = []
        self.transition_track = []
        self.transition_track_directions = []

        self.cached_track_speed = (0, 0)

        # Initializing flags
        self.preloaded_chunk_flag = False
        self.normal_chunk_flag = False
        self.transition_chunk_flag = False

        # Loading first chunk
        self.preload_chunk()
        self.preloaded_chunk = False
        self.load_track_chunk(track_chunk_type=TrackChunkType.NORMAL)

        self.chunk = 0

    def map_direction_to_tile(self, tile_direction):
        if tile_direction == TileDirection.UP:
            return TrackTile(
                corner_x=0,
                corner_y=-self.tile_size,
                tile_size=self.tile_size,
                direction=tile_direction
            )
        elif tile_direction == TileDirection.DOWN:
            return TrackTile(
                corner_x=0,
                corner_y=self.tile_size,
                tile_size=self.tile_size,
                direction=tile_direction
            )
        elif tile_direction == TileDirection.RIGHT:
            return TrackTile(
                corner_x=self.tile_size,
                corner_y=0,
                tile_size=self.tile_size,
                direction=tile_direction
            )
        elif tile_direction == TileDirection.LEFT:
            return TrackTile(
                corner_x=-self.tile_size,
                corner_y=0,
                tile_size=self.tile_size,
                direction=tile_direction
            )
        else:
            # The first square
            return TrackTile(
                corner_x=-self.tile_size / 2,
                corner_y=-self.tile_size / 2,
                tile_size=self.tile_size,
                direction=tile_direction
            )

    def preload_chunk(self):
        # Calculating if its possible to load a full chunk
        remaining_tiles = len(self.track) - self.chunk
        number_tiles_to_preload = self.chunk_size
        if remaining_tiles < self.chunk_size:
            number_tiles_to_preload = remaining_tiles

        # Preloading tiles
        to_preload_chunk = self.track[self.chunk:number_tiles_to_preload]

        # Creating tiles
        self.cached_track_chunk = list(map(self.map_direction_to_tile, to_preload_chunk))

        # Calculating average track speed
        self.cached_track_speed = (
            sum(list(map(map_direction_to_horizontal_unitary, to_preload_chunk))),
            sum(list(map(map_direction_to_vertical_unitary, to_preload_chunk)))
        )

        # Increase chunk index
        self.chunk += self.chunk_size

        # Set Flag
        self.preloaded_chunk = True

    def load_track_chunk(self, track_chunk_type):
        if track_chunk_type == TrackChunkType.NORMAL:
            # Calculating new center for the  transition track
            offset_x = sum(
                list(map(lambda x: map_direction_to_horizontal_unitary(x.direction), self.transition_track))
            ) * self.tile_size
            offset_y = sum(
                list(map(lambda x: map_direction_to_vertical_unitary(x.direction), self.transition_track))
            ) * self.tile_size

            self.pivot_normal = np.add(self.pivot_transition, (-offset_x, offset_y))

            # Loading new normal track chunk
            self.normal_track = self.cached_track_chunk[0:self.normal_track_size]

            # Modifying flags
            self.normal_chunk_flag = True
            self.transition_chunk_flag = False
            self.preloaded_chunk_flag = False

        elif track_chunk_type == TrackChunkType.TRANSITION:
            # Calculating new center for the  transition track
            offset_x = sum(
                list(map(lambda x: map_direction_to_horizontal_unitary(x.direction), self.normal_track))
            ) * self.tile_size
            offset_y = sum(
                list(map(lambda x: map_direction_to_vertical_unitary(x.direction), self.normal_track))
            ) * self.tile_size

            print(self.pivot_transition)
            self.pivot_transition = np.add(self.pivot_normal, (-offset_x, offset_y))
            print(self.pivot_transition)

            # Loading new transition track chunk
            self.transition_track = self.cached_track_chunk[self.normal_track_size:]

            # Modifying flags
            self.normal_chunk_flag = False
            self.transition_chunk_flag = True
        else:
            raise Exception("Error in 'load_track_chunk': Unknown {} TrackChunkType detected".format(track_chunk_type))

    def translate(self, speed):
        # Move both centers
        self.pivot_normal = np.add(self.pivot_normal, speed)

        self.pivot_transition = np.add(self.pivot_normal, speed)

    def draw(self, tile_index):
        # Checking if its necessary to preload
        next_index_tile = tile_index % 8
        print(next_index_tile, self.preloaded_chunk_flag)
        if next_index_tile == 6 and self.normal_chunk_flag:
            self.load_track_chunk(track_chunk_type=TrackChunkType.NORMAL)
        elif next_index_tile == 2 and self.transition_chunk_flag:
            self.load_track_chunk(track_chunk_type=TrackChunkType.TRANSITION)
        elif next_index_tile == 4 and not self.preloaded_chunk_flag:
            self.preload_chunk()

        with push_matrix():
            # Drawing Normal track
            translate(self.pivot_normal[0], self.pivot_normal[1])
            for normal_track_tile in self.normal_track:
                draw_track_tile(normal_track_tile)

        with push_matrix():
            # Drawing Transition track
            translate(self.pivot_transition[0], self.pivot_transition[1])
            for transition_track_tile in self.transition_track:
                draw_track_tile(transition_track_tile)


class TrackTile:
    def __init__(self, corner_x, corner_y, tile_size, direction):
        # Tile Definition
        self.corner_x = corner_x
        self.corner_y = corner_y
        self.tile_size = tile_size
        self.direction = direction
