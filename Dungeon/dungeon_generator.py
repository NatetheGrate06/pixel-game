# Dungeon/dungeon_generator.py
from Dungeon.room import Room, GenerateRoom
import random
import math

MAX_ROOMS = 15   # how many rooms per floor

class DungeonGenerator:
    def __init__(self, num_rooms=MAX_ROOMS):
        self.num_rooms = num_rooms
        self.rooms: list[Room] = []

    # -------- PUBLIC --------
    def generate_new_floor(self):
        """Create a new random layout of rooms."""
        self.rooms = []
        self._generate_rooms()
        self._connect_rooms()
        self._assign_special_rooms()

    # -------- INTERNAL STEPS --------
    def _generate_rooms(self):
        self.rooms = []
    
        for _ in range(self.num_rooms):
            x = random.randint(0, 1000)
            y = random.randint(0, 800)

            room = Room("Normal")
            room.position = (x, y)
            room.neighbors = []
            room.is_start = False
            room.is_boss = False

            self.rooms.append(room)

    def _connect_rooms(self):
        """Connect rooms in a minimally connected graph, plus some extra links."""
        if not self.rooms:
            return

        unvisited = self.rooms.copy()
        visited = [unvisited.pop(0)]

        # connect each unvisited room to the nearest visited one
        while unvisited:
            uv = unvisited.pop(0)
            closest = min(visited, key=lambda r: self._distance(r, uv))

            uv.neighbors.append(closest)
            closest.neighbors.append(uv)
            visited.append(uv)

        # add a few extra random connections
        extra_edges = self.num_rooms // 3
        for _ in range(extra_edges):
            r1, r2 = random.sample(self.rooms, 2)
            if r2 not in r1.neighbors:
                r1.neighbors.append(r2)
                r2.neighbors.append(r1)

        for room in self.rooms :
            room.load_doors()

    def _assign_special_rooms(self):
        """Mark one start room, one boss room, and one treasure room."""
        if not self.rooms:
            return

        # start = room with smallest x
        start_room = min(self.rooms, key=lambda r: r.position[0])
        start_room.room_type = "Start"
        start_room.is_start = True

        # boss = farthest from start
        boss_room = max(self.rooms, key=lambda r: self._distance(start_room, r))
        boss_room.room_type = "Boss"
        boss_room.is_boss = True

        # treasure = random remaining room
        leftovers = [r for r in self.rooms if r not in (start_room, boss_room)]
        if leftovers:
            treasure_room = random.choice(leftovers)
            treasure_room.room_type = "Treasure"

    # -------- HELPERS --------
    def _distance(self, r1, r2):
        x1, y1 = r1.position
        x2, y2 = r2.position
        return math.dist((x1, y1), (x2, y2))

    # -------- API USED BY OTHER SYSTEMS --------
    def get_start_room(self):
        for room in self.rooms:
            if getattr(room, "is_start", False):
                return room
        return None

    def get_random_room(self, exclude=None):
        choices = [room for room in self.rooms if room is not exclude]
        return random.choice(choices) if choices else None

    def update(self, dt):
        for room in self.rooms:
            room.update(dt)

    def get_neighbor(self, room, direction):
        if direction not in room.doors:
            return None

        rx, ry = room.position
        best = None
        best_dist = 999999

        for nbr in room.neighbors:
            nx, ny = nbr.position

            if direction == "N" and ny < ry:
                d = abs(ry - ny)
            elif direction == "S" and ny > ry:
                d = abs(ry - ny)
            elif direction == "E" and nx > rx:
                d = abs(nx - rx)
            elif direction == "W" and nx < rx:
                d = abs(nx - rx)
            else:
                continue

            if d < best_dist:
                best = nbr
                best_dist = d

        return best

import pygame

class DungeonVisualizer:
    """Simple minimap / debug view of the dungeon graph."""
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.scale = 0.2
        self.offset_x = 50
        self.offset_y = 100
        self.font = pygame.font.Font(None, 18)

    def draw(self, surface, current_room):
        if not self.dungeon.rooms:
            return  # nothing to draw

        # print only once per frame is normal, but we can comment this out later
        # print("Drawing map...")

        # --- draw connections ---
        for room in self.dungeon.rooms:
            x1 = int(room.position[0] * self.scale + self.offset_x)
            y1 = int(room.position[1] * self.scale + self.offset_y)

            for nbr in room.neighbors:
                x2 = int(nbr.position[0] * self.scale + self.offset_x)
                y2 = int(nbr.position[1] * self.scale + self.offset_y)
                pygame.draw.line(surface, (120, 120, 120), (x1, y1), (x2, y2), 2)

        # --- draw room nodes ---
        for room in self.dungeon.rooms:
            x = int(room.position[0] * self.scale + self.offset_x)
            y = int(room.position[1] * self.scale + self.offset_y)

            if room is current_room :
                color = (50, 150, 255)
            elif room.room_type == "Start":
                color = (0, 255, 0)
            elif room.room_type == "Boss":
                color = (255, 0, 0)
            elif room.room_type == "Treasure":
                color = (255, 215, 0)
            else:
                color = (180, 180, 180)

            pygame.draw.circle(surface, color, (x, y), 7)

            # tiny label with first letter of type
            label_char = room.room_type[0] if room.room_type else "N"
            label = self.font.render(label_char, True, (0, 0, 0))
            label_rect = label.get_rect(center=(x, y))
            surface.blit(label, label_rect)
