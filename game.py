import pygame
import random

from Dungeon.room import Room, GenerateRoom
from Dungeon.dungeon_generator import DungeonGenerator, DungeonVisualizer
from Entities.player import Player
from UI.ui_manager import UIManager
from UI.game_state_manager import GameStateManager
from UI.main_menu import Menu
from Entities.projectile import Projectile, Cursor
from UI.Settings.resolution_manager import ResolutionManager

class Game:
    def __init__(self):
        pygame.init()

        self.resolution = ResolutionManager()
        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
        self.resolution.apply_resolution(800, 450)

        pygame.display.set_caption("BIOS4096")

        self.clock = pygame.time.Clock()
        self.running = True
        pygame.mouse.set_visible(False)

        # State Manager
        self.state_manager = GameStateManager()

        # Game systems
        self.player = Player(self)
        self.dungeon = DungeonGenerator()
        self.dungeon.generate_new_floor() 
        
        self.current_room = self.dungeon.get_start_room()

        self.ui = UIManager(self.player, self)

        # Minimap (Visualizer)
        self.minimap = DungeonVisualizer(self.dungeon)

        # Main menu
        self.menu = Menu(self.screen, self.state_manager)

        self.cursor = Cursor(self)

        self.tiles = GenerateRoom.load_tileset("Assets/Images/mainlevbuild.png")

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

                if event.type == pygame.VIDEORESIZE :
                    self.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )
                    self.resolution.apply_resolution(event.w, event.h)

            # Different game states
            if self.state_manager.state == "MAIN_MENU":
                self.menu.update(events)
                self.menu.draw()
                self.cursor.draw(self.screen)
                self.cursor.update()

            elif self.state_manager.state == "GAME":
                self.update(dt)
                self.draw()

            pygame.display.flip()

    # ---------------------------------------------------------
    # GAME UPDATE
    # ---------------------------------------------------------
    def update(self, dt):
        self.player.update(dt, self.current_room.walls)
        self.dungeon.update(dt)
        self.ui.update(dt)
        self.cursor.update()

    # ---------------------------------------------------------
    # RENDER
    # ---------------------------------------------------------
    def draw(self):
        self.screen.fill((15, 15, 20))

        # Draw room first (so walls appear behind player)
        self.current_room.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # Draw dungeon minimap
        self.minimap.draw(self.screen)

        # Draw UI
        self.ui.draw(self.screen)

        # Draw cursor last (always on top)
        self.cursor.draw(self.screen)

    # ---------------------------------------------------------
    # START GAME
    # ---------------------------------------------------------
    def start_game(self):
        self.dungeon.generate_new_floor()     # creates rooms

        # recreate minimap after new floor generation
        self.minimap = DungeonVisualizer(self.dungeon)
        
        # set starting room
        self.current_room = self.dungeon.get_start_room()

        # initialize player position
        self.player.spawn_at(self.current_room)

        self.state_manager.change_state("GAME")


# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.main_loop()
    print("\nScanning tilesheet...\n")
    GenerateRoom.detect_floor_tile_block("Assets/Images/mainlevbuild.png")