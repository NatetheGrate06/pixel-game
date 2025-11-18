import pygame

class Room:
    def __init__(self, room_type="Normal"):
        self.room_type = room_type
        self.is_start = False
        self.is_boss = False
        self.position = (0, 0)
        self.neighbors = []
        self.entities = []

        self.width = 1000
        self.height = 800

        self.spawn_point = (200, 200)
        self.walls = []

        self.generate_walls()

    def update(self, dt):
        for entity in self.entities:
            if hasattr(entity, "update"):
                entity.update(dt)

    def draw(self, surface):
        for wall in self.walls:
            pygame.draw.rect(surface, (255, 0, 0), wall)

    def generate_walls(self) :
        x, y = self.position
        w, h = self.width, self.height

        self.walls = [
            pygame.Rect(200, 0, 800, 20), 
            pygame.Rect(0, 580, 800, 20),
            pygame.Rect(200, 0, 20, 600), 
            pygame.Rect(780, 0, 20, 600),
        ]