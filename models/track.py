from p5 import *
from dance_fire_ice.utils.constants import *
import numpy as np
from math import ceil


def draw_track_tile(tile):
    # Translate to the corresponding tile corner
    translate(tile.corner_x, tile.corner_y)

    # Draw tile
    rect((0, 0), tile.tile_size, tile.tile_size)


class Track:
    def __init__(self, pivot_x, pivot_y, tile_size, track):
        # Initializing track
        self.track = track
        self.total_tiles = len(track)
        self.tile_size = tile_size

        # Initializing constant tiles objects for drawing
        self.TILE_UP = TrackTile(
            corner_x=0,
            corner_y=-self.tile_size,
            tile_size=self.tile_size,
            direction=TileDirection.UP
        )
        self.TILE_DOWN = TrackTile(
            corner_x=0,
            corner_y=self.tile_size,
            tile_size=self.tile_size,
            direction=TileDirection.DOWN
        )
        self.TILE_RIGHT = TrackTile(
            corner_x=self.tile_size,
            corner_y=0,
            tile_size=self.tile_size,
            direction=TileDirection.RIGHT
        )
        self.TILE_LEFT = TrackTile(
            corner_x=-self.tile_size,
            corner_y=0,
            tile_size=self.tile_size,
            direction=TileDirection.LEFT
        )
        self.TILE_INITIAL = TrackTile(
            corner_x=-self.tile_size / 2,
            corner_y=-self.tile_size / 2,
            tile_size=self.tile_size,
            direction=TileDirection.INITIAL
        )

        # Initializing track centers
        self.starting_x = pivot_x
        self.starting_y = pivot_y
        self.pivot_normal = (self.starting_x, self.starting_y)
        self.pivot_transition = (self.starting_x, self.starting_y)

        # Initializing constants
        self.normal_track_size = 8
        self.transition_track_size = 8
        self.chunk_size = self.normal_track_size + self.transition_track_size

        self.when_to_preload = self.chunk_size - 4
        self.when_to_load_transition = self.normal_track_size - 2
        self.when_to_load_normal = self.chunk_size - 2

        # Initializing tracks
        self.cached_track_chunk = []

        self.normal_track = []
        self.normal_track_directions = []
        self.transition_track = []
        self.transition_track_directions = []

        # Calculating total chunks
        total_full_chunks = len(self.track) // self.chunk_size
        remaining_tiles = len(self.track) % self.chunk_size
        self.total_normal_track_chunks = total_full_chunks + (1 if remaining_tiles > 0 else 0)
        self.total_transition_track_chunks = total_full_chunks + (1 if remaining_tiles > self.normal_track_size else 0)

        # Initializing flags
        self.preloaded_chunk_flag = False
        self.normal_chunk_flag = False
        self.transition_chunk_flag = False
        self.no_more_chunks_flag = False

        # Initializing counters
        self.tile_counter = 0
        self.normal_track_chunk_counter = 0
        self.transition_track_chunk_counter = 0

        # Loading first chunk
        self.preload_chunk()
        self.no_more_chunks_flag = False

        self.load_track_chunk(track_chunk_type=TrackChunkType.NORMAL)
        self.load_track_chunk(track_chunk_type=TrackChunkType.TRANSITION)

        self.transition_track_chunk_counter -= 1

    def reset(self):
        # Resetting position
        self.pivot_normal = (self.starting_x, self.starting_y)
        self.pivot_transition = (self.starting_x, self.starting_y)

        # Resetting Flags
        self.preloaded_chunk_flag = False
        self.normal_chunk_flag = False
        self.transition_chunk_flag = False
        self.no_more_chunks_flag = False

        # Resetting Counters
        self.tile_counter = 0
        self.normal_track_chunk_counter = 0
        self.transition_track_chunk_counter = 0

        # Resetting tracks
        self.normal_track.clear()
        self.transition_track.clear()

        # Loading first chunk
        self.preload_chunk()
        self.no_more_chunks_flag = False

        self.load_track_chunk(track_chunk_type=TrackChunkType.NORMAL)
        self.load_track_chunk(track_chunk_type=TrackChunkType.TRANSITION)

        self.transition_track_chunk_counter -= 1

    def map_direction_to_tile(self, tile_direction):
        if tile_direction == TileDirection.UP:
            return self.TILE_UP
        elif tile_direction == TileDirection.DOWN:
            return self.TILE_DOWN
        elif tile_direction == TileDirection.RIGHT:
            return self.TILE_RIGHT
        elif tile_direction == TileDirection.LEFT:
            return self.TILE_LEFT
        else:
            # The first square
            return self.TILE_INITIAL

    def preload_chunk(self):
        # Calculating if its possible to load a full chunk
        remaining_tiles = len(self.track) - self.tile_counter
        tiles_to_preload_limit = self.chunk_size
        if remaining_tiles < self.chunk_size:
            tiles_to_preload_limit = remaining_tiles
        tiles_to_preload_limit += self.tile_counter

        # Preloading tiles
        to_preload_chunk = self.track[self.tile_counter:tiles_to_preload_limit]

        # Creating tiles
        self.cached_track_chunk = list(map(self.map_direction_to_tile, to_preload_chunk))

        # Increase chunk index
        self.tile_counter = tiles_to_preload_limit

        # Set Flag
        self.no_more_chunks_flag = self.tile_counter == self.total_tiles
        self.preloaded_chunk_flag = True

    def load_track_chunk(self, track_chunk_type):
        if track_chunk_type == TrackChunkType.NORMAL:
            if self.normal_track_chunk_counter < self.total_normal_track_chunks:
                # Loading new normal track chunk
                self.normal_track = self.cached_track_chunk[0:self.normal_track_size]

                # Calculating new center for the transition track
                offset_x = (sum(
                    list(map(lambda x: map_direction_to_horizontal_unitary(x.direction), self.transition_track))
                ) + map_direction_to_horizontal_unitary(self.normal_track[0].direction)) * self.tile_size
                offset_y = (sum(
                    list(map(lambda x: map_direction_to_vertical_unitary(x.direction), self.transition_track))
                ) + map_direction_to_vertical_unitary(self.normal_track[0].direction)) * self.tile_size

                # Moving to new center
                self.pivot_normal = np.add(self.pivot_transition, (offset_x, offset_y))

                # Setting first tile as Initial
                self.normal_track[0] = self.TILE_INITIAL

                # Modifying flags
                self.normal_chunk_flag = True
                self.transition_chunk_flag = False
                self.preloaded_chunk_flag = False

                # Increasing counter
                self.normal_track_chunk_counter += 1
            else:
                self.normal_track.clear()

        elif track_chunk_type == TrackChunkType.TRANSITION:
            if self.transition_track_chunk_counter < self.total_transition_track_chunks:
                # Loading new transition track chunk
                self.transition_track = self.cached_track_chunk[self.normal_track_size:]

                # Calculating new center for the  transition track
                offset_x = (sum(
                    list(map(lambda x: map_direction_to_horizontal_unitary(x.direction), self.normal_track))
                ) + map_direction_to_horizontal_unitary(self.transition_track[0].direction)) * self.tile_size
                offset_y = (sum(
                    list(map(lambda x: map_direction_to_vertical_unitary(x.direction), self.normal_track))
                ) + map_direction_to_vertical_unitary(self.transition_track[0].direction)) * self.tile_size

                # Moving to new center
                self.pivot_transition = np.add(self.pivot_normal, (offset_x, offset_y))

                # Setting first tile as Initial
                self.transition_track[0] = self.TILE_INITIAL

                # Modifying flags
                self.normal_chunk_flag = False
                self.transition_chunk_flag = True

                # Increasing counter
                self.transition_track_chunk_counter += 1
            else:
                self.transition_track.clear()
        else:
            raise Exception("Error in 'load_track_chunk': Unknown {} TrackChunkType detected".format(track_chunk_type))

    def translate(self, speed):
        # Move both centers
        self.pivot_normal = np.add(self.pivot_normal, speed)

        self.pivot_transition = np.add(self.pivot_transition, speed)

    def draw(self, tile_index):
        # Checking if its necessary to preload
        next_index_tile = tile_index % self.chunk_size
        if next_index_tile == self.when_to_load_normal and not self.normal_chunk_flag:
            self.load_track_chunk(track_chunk_type=TrackChunkType.NORMAL)
        elif next_index_tile == self.when_to_load_transition and not self.transition_chunk_flag:
            self.load_track_chunk(track_chunk_type=TrackChunkType.TRANSITION)
        elif next_index_tile == self.when_to_preload and not self.preloaded_chunk_flag:
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
