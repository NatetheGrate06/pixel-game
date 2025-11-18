import pygame
import random

from Dungeon.dungeon_generator import DungeonGenerator, DungeonVisualizer
from Entities.player import Player
from UI.ui_manager import UIManager
from UI.game_state_manager import GameStateManager
from UI.main_menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1600, 900))
        pygame.display.set_caption("BIOS4096")

        self.clock = pygame.time.Clock()
        self.running = True

        self.state_manager = GameStateManager()

        self.player = Player()
        self.dungeon = DungeonGenerator()
        self.dungeon.generate_new_floor() 
        self.ui = UIManager(self.player)
        self.dungeon_map = DungeonVisualizer(self.dungeon)

        self.menu = Menu(self.screen, self.state_manager)

    # ---------------------------------------------------------
    # MAIN GAME LOOP
    # ---------------------------------------------------------
    def main_loop(self):
        while self.running:
            dt = self.clock.tick(60) / 1000  # delta time in seconds
            events = pygame.event.get()

            # Global events
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # Different game states
            if self.state_manager.state == "MAIN_MENU":
                self.menu.update(events)
                self.menu.draw()

            elif self.state_manager.state == "GAME":
                self.update(dt)
                self.draw()

            pygame.display.flip()

    # ---------------------------------------------------------
    # GAME UPDATE
    # ---------------------------------------------------------
    def update(self, dt):
        self.player.update(dt)
        self.dungeon.update(dt)
        self.ui.update(dt)

    # ---------------------------------------------------------
    # RENDER
    # ---------------------------------------------------------
    def draw(self):
        self.screen.fill((15, 15, 20))
        self.dungeon_map.draw(self.screen)
        self.player.draw(self.screen)
        self.ui.draw(self.screen)

    # ---------------------------------------------------------
    # START GAME
    # ---------------------------------------------------------
    def start_game(self):
        self.dungeon.generate_new_floor()     # creates rooms
        self.visualizer = DungeonVisualizer(self.dungeon)   # recreate map after generation
        
        start = self.dungeon.get_start_room()
        self.player.initialize()
        self.player.spawn_at(start)

        self.state_manager.change_state("GAME")


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.main_loop()
