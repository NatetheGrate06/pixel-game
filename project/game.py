import pygame
import random

from Dungeon.dungeon_generator import DungeonGenerator
from Entities.player import Player
from UI.ui_manager import UIManager
from UI.game_state_manager import GameStateManager
from UI.main_menu import Menu

class Game:
    def __init__(self):
        pygame.init()

        # Window
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Dungeon Crawler")

        self.clock = pygame.time.Clock()
        self.running = True
        
        # State Manager
        self.state_manager = GameStateManager()

        # Game systems
        self.player = Player()
        self.dungeon = DungeonGenerator()
        self.ui = UIManager(self.player)

        # Main menu
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
        self.dungeon.draw(self.screen)
        self.player.draw(self.screen)
        self.ui.draw(self.screen)

    # ---------------------------------------------------------
    # START GAME
    # ---------------------------------------------------------
    def start_game(self):
        """Called once when switching from menu to gameplay."""
        self.dungeon.generate_new_floor()
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
