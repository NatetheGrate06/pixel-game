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
        self.tilemap = GenerateRoom.generate_random_room()

    def update(self, dt):
        for entity in self.entities:
            if hasattr(entity, "update"):
                entity.update(dt)

    def draw(self, surface, tiles):
        for wall in self.walls:
            pygame.draw.rect(surface, (255, 0, 0), wall)

        for y, row in enumerate(self.tilemap) :
            for x, tile_index in enumerate(row) :
                tile = tiles[tile_index]
                surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))

    def generate_walls(self) :
        x, y = self.position
        w, h = self.width, self.height

        WT = 20  # wall thickness

        self.walls = [
            pygame.Rect(0, 0, 1600, WT),          # top
            pygame.Rect(0, 900 - WT, 1600, WT),   # bottom
            pygame.Rect(0, 0, WT, 900),           # left
            pygame.Rect(1600 - WT, 0, WT, 900),   # right
        ]
import pygame
import random

TILE_SIZE = 32
ROOM_WIDTH = 20
ROOM_HEIGHT = 15

#TODO these are just stand-ins for now
FLOORS = [30, 31, 32, 33, 34, 35]
WALLS = [5, 6, 7, 8, 9, 10]
CORNERS = [0, 1, 2, 3]
DOORS = [40, 41, 42]

class GenerateRoom :

    def load_tileset(path) :
        tileset = pygame.image.load(path).convert_alpha()
        tiles = []

        tileset_width = tileset.get_width() // TILE_SIZE
        tileset_height = tileset.get_height() // TILE_SIZE

        for y in range(tileset_height) :
            for x in range(tileset_width) :
                tile = tileset.subsurface(
                    (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )

                tiles.append(tile)

        return tiles

    def generate_random_room() :
        room = [[None for _ in range(ROOM_WIDTH)] for _ in range(ROOM_HEIGHT)]

        for y in range(ROOM_HEIGHT) :
            for x in range(ROOM_WIDTH) :

                if y == 0 or y == ROOM_HEIGHT - 1 or x == 0 or x == ROOM_WIDTH - 1:
                    room[y][x] = random.choice(WALLS)

                else :
                    room[y][x] = random.choice(FLOORS)

        return room
