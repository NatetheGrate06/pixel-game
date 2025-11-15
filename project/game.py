import pygame
import random
from Dungeon.dungeon_generator import DungeonGenerator
from Entities.player import Player
from UI.ui_manager import UIManager
from UI.game_state_manager import GameStateManager
from UI.main_menu import Menu

player = Player()
ui = UIManager(player)
running = False


class game:

    def __init__(self) :
        self.dungeon = DungeonGenerator()
        self.player = Player()
        self.ui = UIManager()

    #TODO just need to entirely fix this
    def start_game(self) :
        running = True
        self.dungeon.generate_new_floor()
        start_room = self.dungeon.get_start_room()
        self.player.initialize()
        self.player.spawn_at(start_room)

        while (running) :
            if GameStateManager.STATES.state == "MAIN MENU" :
                Menu.update()
                Menu.draw()
            elif GameStateManager.STATES.state == "GAME" :
                self.start_game
        
    def update(self, dt) :
        self.player.update(dt)
        self.dungeon.update(dt)

    def main(self) :
        self.screen = pygame.display.set_mode((800, 600))
        