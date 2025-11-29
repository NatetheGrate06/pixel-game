import pygame

class Room:
    def __init__(self, room_type="Normal"):
        self.room_type = room_type
        self.is_start = False
        self.is_boss = False
        self.position = (0, 0)
        self.neighbors = []
        self.entities = []

        self.width = 1600
        self.height = 800

        self.spawn_point = (200, 200)
        self.walls = []

        self.generate_walls()

        # Load everything required
        self.floor_tiles = GenerateRoom.load_floor_tiles("Assets/Images/mainlevbuild.png")
        self.tilemap = GenerateRoom.generate_random_room()

        self.floor_tiles = GenerateRoom.load_floor_tiles("Assets/Images/floor_tiles.png")
        self.top_walls = GenerateRoom.load_top_walls("Assets/Images/crypt-wall.png", scale=2)

    def update(self, dt):
        pass

    def draw_top_walls(self, surface, room_pixel_width):
        x = 0
        i = 0
        tiles = self.top_walls

        while x < room_pixel_width:
            wall = tiles[i % len(tiles)]
            surface.blit(wall, (x, 0))
            x += wall.get_width()
            i += 1

    #TODO draw rest of room

    def draw(self, surface):
        TILE_SIZE = 16

        for y, row in enumerate(self.tilemap):
            for x, tile_index in enumerate(row):

                if tile_index is None:
                    continue

                if tile_index < 0 or tile_index >= len(self.floor_tiles):
                    continue  # safety check

                tile = self.floor_tiles[tile_index]
                surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
        
        room_pixel_width = len(self.tilemap[0]) * TILE_SIZE
        self.draw_top_walls(surface, room_pixel_width)

        # Debug walls (optional)
        # for wall in self.walls:
        #     pygame.draw.rect(surface, (255, 0, 0), wall, 1)

    def generate_walls(self):
        WT = 20  # wall thickness

        self.walls = [
            pygame.Rect(0, 0, 1600, WT),
            pygame.Rect(0, 900 - WT, 1600, WT),
            pygame.Rect(0, 0, WT, 900),
            pygame.Rect(1600 - WT, 0, WT, 900),
        ]

import pygame
import random

TILE_SIZE = 8
ROOM_WIDTH = 100
ROOM_HEIGHT = 58

# For now, just use all 36 floor tiles
FLOORS = list(range(151))
WALLS = [0, 1, 2, 3, 4, 5]   # we'll just re-use some floor tiles as walls for now
CORNERS = [0, 1, 2, 3]
DOORS = [0]                  # placeholder

class GenerateRoom:

    @staticmethod
    def load_tileset(path):
        tileset = pygame.image.load(path).convert_alpha()
        tiles = []

        tileset_width = tileset.get_width() // TILE_SIZE
        tileset_height = tileset.get_height() // TILE_SIZE

        for y in range(tileset_height):
            for x in range(tileset_width):
                tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                tile.blit(tileset, (0, 0),
                          (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                tiles.append(tile)

        return tiles

    @staticmethod
    def generate_random_room():
        room = [[None for _ in range(ROOM_WIDTH)] for _ in range(ROOM_HEIGHT)]

        for y in range(ROOM_HEIGHT):
            for x in range(ROOM_WIDTH):

                # borders = walls
                if y == 0 or y == ROOM_HEIGHT - 1 or x == 0 or x == ROOM_WIDTH - 1:
                    room[y][x] = random.choice(WALLS)
                else:
                    room[y][x] = random.choice(FLOORS)

        return room

    @staticmethod
    def load_floor_tiles(path):
        TILE_SIZE = 16  # each tile is 16x16

        sheet = pygame.image.load(path).convert_alpha()
        sheet_width = sheet.get_width()

        tile_count = sheet_width // TILE_SIZE
        tiles = []

        for i in range(tile_count):
            tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            tile.blit(sheet, (0, 0), (i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
            tiles.append(tile)

        print(f"Loaded {len(tiles)} floor tiles")
        return tiles
    
    @staticmethod
    def load_top_walls(path, scale=2):
        img = pygame.image.load(path).convert_alpha()
        w, h = img.get_width(), img.get_height()

        # Split into two equal pieces
        section_w = w // 2

        wall_tiles = []

        for i in range(2):
            part = pygame.Surface((section_w, h), pygame.SRCALPHA)
            part.blit(img, (0, 0), (i * section_w, 0, section_w, h))

            # Scale walls to match your 32x32 tile scale
            if scale != 1:
                part = pygame.transform.scale(
                    part,
                    (part.get_width() * scale, part.get_height() * scale)
                )

            wall_tiles.append(part)

        return wall_tiles