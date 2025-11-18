import pygame

class Room:
    def __init__(self, room_type="Normal"):
        self.room_type = room_type
        self.is_start = False
        self.is_boss = False
        self.position = (0, 0)
        self.neighbors = []
        self.entities = []
        self.spawn_point = (200, 200)
        self.walls = []

    def update(self, dt):
        for entity in self.entities:
            if hasattr(entity, "update"):
                entity.update(dt)

    def draw(self, surface):
        pass
