import pygame

class Room: 

    def __init__(self, is_start=False, is_boss=False) :
        self.is_start = is_start
        self.is_boss = is_boss
        
        self.enemies = []
        self.loot = []

        self.width = 400
        self.height = 100

        self.spawn_point = pygame.Vector2(100, 100)

    def enter(self):
        #TODO combat logic
        pass

    def update(self, dt) :
        for enemy in self.enemies:
            enemy.update(dt)

    def get_width() :
        return self.width
    
    def get_height() :
        return self.height