import pygame
import random

from Dungeon.room import Room, GenerateRoom
from Dungeon.dungeon_generator import DungeonGenerator, DungeonVisualizer
from Entities.player import Player
from Entities.weapon import Weapon, Gun, Melee
from Entities.enemy import Enemy, Boss, Brute, Grunt
from UI.ui_manager import UIManager
from UI.game_state_manager import GameStateManager
from UI.main_menu import Menu
from UI.Settings.settings_menu import SettingsMenu
from UI.credits import CreditsMenu
from Entities.projectile import Projectile, Cursor
from UI.Settings.resolution_manager import ResolutionManager
from Items.inventory import Inventory
from Items.upgrade import Upgrade
from Assets import sound_manager
from Assets.music_manager import MusicManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.resolution = ResolutionManager()
        self.screen = pygame.display.set_mode((1600, 900), pygame.RESIZABLE)
        self.resolution.apply_resolution(1600, 900)

        pygame.display.set_caption("BIOS4096")

        Upgrade.load_icons()

        sound_manager.load_sounds()

        self.music = MusicManager()

        #pygame.mixer.music.load("Assets/Music/main_theme.mp3")
        #pygame.mixer.music.play(-1)
        #pygame.mixer.music.set_volume(1.0)

        #self.sfx_volume = 1.0

        self.clock = pygame.time.Clock()
        self.running = True
        pygame.mouse.set_visible(False)

        self.music.play("menu")

        # State Manager
        self.state_manager = GameStateManager()

        # Settings Menu
        self.settings_menu = SettingsMenu(self.screen, self.state_manager, self)

        # Credits Menu
        self.credits_menu = CreditsMenu(self)

        # Game systems
        self.player = Player(self)
        self.dungeon = DungeonGenerator()
        self.dungeon.generate_new_floor() 

        # instantiate for rooms
        for room in self.dungeon.rooms:
            room.game = self
        
        self.current_room = self.dungeon.get_start_room()
        #self.current_room = Room("Treasure")

        self.ui = UIManager(self.player, self)

        # Minimap (Visualizer)
        self.minimap = DungeonVisualizer(self.dungeon)

        # Main menu
        self.menu = Menu(self.screen, self.state_manager, self)

        self.cursor = Cursor(self)

        self.tiles = GenerateRoom.load_tileset("Assets/Images/mainlevbuild.png")

        self.enemies = []

        self.projectiles = []

        self.player.equip_weapon(Gun(damage=10, speed=450))
        self.player.equip_weapon(Melee(damage=25, range_=150))

        self.inventory = Inventory()
        self.player.inventory = self.inventory
    
    # ---------------------------------------------------------
    # MAIN GAME LOOP
    # ---------------------------------------------------------
    def main_loop(self):
        while self.running:

            dt = self.clock.tick(60) / 1000  # delta time in seconds
            self.events = pygame.event.get()

            # Global events
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.VIDEORESIZE :
                    self.screen = pygame.display.set_mode(
                        (event.w, event.h), pygame.RESIZABLE
                    )
                    self.resolution.apply_resolution(event.w, event.h)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        print("Resetting floor...")
                        self.start_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state_manager.state == "GAME":
                            self.reset_menu()
                        else:
                            self.state_manager.change_state("MAIN_MENU")
                            
            # Different game states
            if self.state_manager.state == "MAIN_MENU":
                self.menu.update(self.events)
                self.menu.draw()
                self.cursor.draw(self.screen)
                self.cursor.update()

            elif self.state_manager.state == "GAME":
                self.update(dt)
                self.draw()

            elif self.state_manager.state == "SETTINGS":
                self.settings_menu.update(self.events)
                self.settings_menu.draw()
                self.cursor.draw(self.screen)
                self.cursor.update()
            elif self.state_manager.state == "CREDITS":
                self.credits_menu.update(dt, self.events)
                self.credits_menu.draw(self.screen)

            pygame.display.flip()

    def brute_killed(self, brute) :
        heal_amount = 10

        self.player.hp += heal_amount
        if self.player.hp > 100:
            self.player.hp = 100

    def spawn_enemies(self, room) :
        print("Spawning enemies.")

        self.enemies = []

        total_min = 0
        total_max = 6
        total_enemies = random.randint(total_min, total_max)

        max_brutes = min(2, total_enemies)
        num_brutes = random.randint(0, max_brutes)

        num_grunts = total_enemies - num_brutes

        for _ in range(num_brutes) :
            print("Spawing brutes")
            brute = Brute(room)
            brute.on_death_callback = self.brute_killed
            self.enemies.append(brute)
            room.entities.append(brute)

        for _ in range(num_grunts):
            print("Spawning grunts")
            grunt = Grunt(room)
            self.enemies.append(grunt)
            room.entities.append(grunt)

    def reset_menu(self) :
        self.enemies.clear()
        self.projectiles.clear()
        self.state_manager.change_state("MAIN_MENU")

    # ---------------------------------------------------------
    # GAME UPDATE
    # ---------------------------------------------------------
    def update(self, dt):
        self.current_room.visited = True
        self.player.update(dt, self.current_room.walls)
        self.dungeon.update(dt)
        self.ui.update(dt)
        self.cursor.update()

        if self.player.alive == False :
            self.reset_menu()

        for enemy in self.enemies:
            enemy.update(dt, self.player, self.projectiles)
            self.enemies = [e for e in self.enemies if e.alive]

        for p in self.projectiles[:] :
            p.update(dt, self.current_room.walls, self.enemies, self.player)

            if not p.alive:
                self.projectiles.remove(p)

        direction = self.current_room.check_door_collision(self.player.hitbox)

        if direction:
            next_room = self.dungeon.get_neighbor(self.current_room, direction)
            if next_room:
                self.current_room = next_room
                if direction == "N":  # player came from north room - entering from south door
                    self.player.position = pygame.Vector2(next_room.width // 2, next_room.height - 200)

                elif direction == "S":  # came from south - spawn near top
                    self.player.position = pygame.Vector2(next_room.width // 2, 200)

                elif direction == "E":  # came from east - spawn near left
                    self.player.position = pygame.Vector2(200, next_room.height // 2)

                elif direction == "W":  # came from west - spawn near right
                    self.player.position = pygame.Vector2(next_room.width - 200, next_room.height // 2)

                self.player.hitbox.center = self.player.position

                self.enemies.clear()
                if next_room.room_type == "Boss":
                    boss = Boss.spawn_boss(next_room)
                    self.enemies.append(boss)
                else:
                    self.spawn_enemies(next_room)

                print("Moved to room", next_room.position)

        room = self.current_room

        if getattr(room, "has_upgrade", False) :
            upgrade = room.upgrade

            if upgrade.rect.colliderect(self.player.hitbox) :

                upgrade.apply(self.player)
                self.inventory.add_upgrade(upgrade)

                sound_manager.item_pickup.play()

                print(f"Picked up: {upgrade.name}")

                room.has_upgrade = False

    # ---------------------------------------------------------
    # RENDER
    # ---------------------------------------------------------
    def draw(self):
        self.screen.fill((15, 15, 20))

         # Draw room first (so walls appear behind player)
        self.current_room.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        for enemy in self.enemies :
            enemy.draw(self.screen)

        for p in self.projectiles :
            p.draw(self.screen)

        # Draw dungeon minimap
        self.minimap.draw(self.screen, self.current_room)

        # Draw UI
        self.ui.draw(self.screen)

        self.inventory.draw(self.screen)

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

        # initialize player
        self.player.spawn_at(self.current_room)
        self.player.alive = True
        self.player.hp = 100
        self.projectiles.clear()
        self.enemies.clear()

        for w in self.player.weapons :
            w.cooldown_timer = 0
        
        self.player.active_weapon_index = 0

        self.spawn_enemies(self.current_room)

        self.state_manager.change_state("GAME")

        self.music.play("level")

        # reset rooms
        for room in self.dungeon.rooms:
            room.visited = False
            room.entities.clear()

            if room.room_type != "Treasure":
                room.has_upgrade = False
                room.upgrade = None


    # ---------------------------------------------------------
    # Open Settings
    # ---------------------------------------------------------
    def open_settings(self):
        pass

    # ---------------------------------------------------------
    # Open Credits
    # ---------------------------------------------------------
    def open_credits(self):
        pass

# -------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------
if __name__ == "__main__":
    game = Game()
    game.main_loop()
    print("\nScanning tilesheet...\n")