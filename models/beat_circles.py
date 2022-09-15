import numpy as np
import p5

from p5 import *
from p5 import atan
from dance_fire_ice.utils.constants import *


class BeatCircles:
    def __init__(self, frame_rate, bpm, starting_x, starting_y, diameter=10, circle_radius=20):
        # Line Variables
        self.radius = diameter / 2

        # Circle Variables
        self.circle_radius = circle_radius

        # Physics Variables
        hertz = 60/bpm
        half_perimeter_time = (1/hertz)/2
        self.rotation_speed = 2*PI/(half_perimeter_time*frame_rate)
        self.angle = PI
        self.linear_velocity = self.rotation_speed * self.radius
        self.spins = 0

        # Anchor variables
        self.starting_x = starting_x
        self.starting_y = starting_y

        self.position_x = starting_x
        self.position_y = starting_y

        # Anchor variables
        relation = (circle_radius * 0.35) / diameter
        # self.horizontal_threshold = abs(tan(relation))
        # self.vertical_threshold = abs(tan(1 / relation))

        self.threshold_angle = atan(relation)
        self.right_threshold = np.array([0 + self.threshold_angle, TWO_PI - self.threshold_angle])
        self.left_threshold = np.array([PI + self.threshold_angle, PI - self.threshold_angle])
        self.up_threshold = np.array([(3*HALF_PI) + self.threshold_angle, (3*HALF_PI) - self.threshold_angle])
        self.down_threshold = np.array([HALF_PI + self.threshold_angle, HALF_PI - self.threshold_angle])

    def draw(self):
        with push_matrix():
            # Translate to its center
            translate(self.position_x, self.position_y)

            # Rotate
            self.angle += self.rotation_speed
            self.spins += self.angle // TWO_PI
            self.angle = self.angle % TWO_PI
            rotate(self.angle)

            # Draw Anchor circle
            circle(0, 0, self.circle_radius)

            # Draw Circles
            circle(self.radius, 0, self.circle_radius)

    def check_circles_angle(self, next_tile):
        if next_tile == TileDirection.RIGHT:
            return (self.angle <= self.right_threshold[0]) or (self.angle >= self.right_threshold[1])
        elif next_tile == TileDirection.DOWN:
            return (self.angle <= self.down_threshold[0]) and (self.angle >= self.down_threshold[1])
        elif next_tile == TileDirection.LEFT:
            return (self.angle <= self.left_threshold[0]) and (self.angle >= self.left_threshold[1])
        elif next_tile == TileDirection.UP:
            return (self.angle <= self.up_threshold[0]) and (self.angle >= self.up_threshold[1])
        else:
            return False

    def change_anchor(self, tile_direction):
        if self.check_circles_angle(next_tile=tile_direction):
            # Calculating new anchor center and angle
            new_angle = map_direction_to_offset(tile_direction=tile_direction)
            self.position_x += self.radius * cos(new_angle)
            self.position_y += self.radius * sin(new_angle)
            self.angle = new_angle - PI

            return True
        else:
            return False

    def translate(self, speed):
        self.position_x += speed[0]
        self.position_y += speed[1]

    def reset(self):
        # Resetting to the initial position
        self.position_x = self.starting_x
        self.position_y = self.starting_y

        # Resetting angle
        self.angle = PI

        # Resetting spins
        self.spins = 0
