import pygame
import random
from Dungeon.dungeon_generator import DungeonGenerator
from Entities.player import Player
from UI.ui_manager import UIManager

class game:

    def __init__(self) :
        self.dungeon = DungeonGenerator()
        self.player = Player()
        self.ui = UIManager()

    def start_game(self) :
        self.dungeon.generate_new_floor()
        start_room = self.dungeon.get_start_room()
        self.player.initialize()
        self.player.spawn_at(start_room)
        
    def update(self, dt) :
        self.player.update(dt)
        self.dungeon.update(dt)

    def main(self) :
        self.screen = pygame.display.set_mode((800, 600))
        