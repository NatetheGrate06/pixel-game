import pygame 

BASE_WIDTH = 1600
BASE_HEIGHT = 900

class ResolutionManager :
    def __init__(self) :
        self.current_width = BASE_WIDTH
        self.current_height = BASE_HEIGHT

        self.scale_x = 1
        self.scale_y = 1
        self.uniform_scale = 1

    def apply_resolution(self, width, height) :
        self.current_width = width
        self.current_height = height

        self.scale_x = width / BASE_WIDTH
        self.scale_y = height / BASE_HEIGHT

        self.uniform_scale = min(self.scale_x, self.scale_y)

    def scale_value(self, value) :
        return int(value * self.uniform_scale)
    