from p5 import *
from constants import *


class BeatCircles:
    def __init__(self, frame_rate, bpm, position_x, position_y, diameter=10, circle_radius=20):
        # Rotation Variables
        hertz = 60/bpm
        half_perimeter_time = (1/hertz)/2
        self.rotation_speed = 2*PI/(half_perimeter_time*frame_rate)
        self.angle = PI

        # Anchor variables
        self.position_x = position_x
        self.position_y = position_y

        self.anchor_x = 0
        self.anchor_y = 0

        # Line Variables
        self.radius = diameter/2

        # Circle Variables
        self.circle_radius = circle_radius

    def draw(self):
        with push_matrix():
            # Translate to its center
            translate(self.position_x, self.position_y)

            # Rotate
            self.angle += self.rotation_speed
            rotate(self.angle)

            # Draw Anchor circle
            circle(0, 0, self.circle_radius)

            # Draw Circles
            circle(self.radius, 0, self.circle_radius)

    def change_anchor(self, tile_direction):
        new_angle = map_direction_to_offset(tile_direction=tile_direction)
        self.position_x += self.radius*cos(new_angle)
        self.position_y += self.radius*sin(new_angle)
        self.angle = new_angle - PI

        # self.position_x += self.radius*cos(self.angle)
        # self.position_y += self.radius*sin(self.angle)
        # self.angle = self.angle - PI

    def translate(self, speed):
        self.position_x += speed[0]
        self.position_y += speed[1]
