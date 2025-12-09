# Dungeon/dungeon_generator.py
from Dungeon.room import Room, GenerateRoom
from Items.upgrade import Upgrade, UPGRADES
from Entities.enemy import Boss, BOSSES

import random
import math

MAX_ROOMS = 15   # how many rooms per floor

class DungeonGenerator:
    def __init__(self, num_rooms=MAX_ROOMS):
        self.num_rooms = num_rooms
        self.rooms: list[Room] = []
        self.has_upgrade = False

    # -------- PUBLIC --------
    def generate_new_floor(self):
        """Create a new random layout of rooms."""
        self.rooms = []
        self._generate_rooms()
        self._connect_rooms()
        self._assign_special_rooms()

        start_room = self.get_start_room()
        start_room.visited = True

    def _generate_rooms(self):
        """Generate rooms in a clean grid layout."""
        self.rooms = []

        # Create room objects
        for _ in range(self.num_rooms):
            room = Room("Normal")
            room.neighbors = []
            self.rooms.append(room)

        # Assign grid positions
        used_positions = set()
        queue = []

        # Start room placed at (0,0)
        start_room = self.rooms[0]
        start_room.grid_pos = (0, 0)
        used_positions.add((0, 0))
        queue.append(start_room)

        idx = 1

        # BFS placement for all rooms
        while idx < len(self.rooms):
            parent = queue.pop(0)
            px, py = parent.grid_pos

            # Directions: N, E, S, W
            directions = [(0,-1),(1,0),(0,1),(-1,0)]
            random.shuffle(directions)

            for dx, dy in directions:
                if idx >= len(self.rooms): break

                new_pos = (px + dx, py + dy)
                if new_pos in used_positions:
                    continue

                # Assign room
                room = self.rooms[idx]
                room.grid_pos = new_pos
                used_positions.add(new_pos)
                queue.append(room)

                idx += 1

        # Space betwen nodes
        GRID_SIZE = 80  

        for room in self.rooms:
            gx, gy = room.grid_pos
            # Center (0,0)
            room.position = (gx * GRID_SIZE, gy * GRID_SIZE)

    def _connect_rooms(self):
        """Connect rooms in a minimally connected graph."""
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

        for room in self.rooms:
            rx, ry = room.grid_pos

            # Look for neighbors in the 4 cardinal directions
            for other in self.rooms:
                ox, oy = other.grid_pos

                if abs(rx - ox) + abs(ry - oy) == 1:
                    if other not in room.neighbors:
                        room.neighbors.append(other)
                        other.neighbors.append(room)

        # Now load doors
        for room in self.rooms:
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
        boss_room.boss = Boss(random.choice(BOSSES), boss_room)

        # treasure = random remaining room
        leftovers = [r for r in self.rooms if r not in (start_room, boss_room)]
        if leftovers:
            treasure_room = random.choice(leftovers)
            treasure_room.room_type = "Treasure"
            treasure_room.is_treasure = True
            treasure_room.upgrade = random.choice(UPGRADES)
            treasure_room.has_upgrade = True

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

import pygame
from collections import deque

class DungeonVisualizer:
    """Simple minimap / debug view of the dungeon graph."""
    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.room_layout = {}   
        self.grid_spacing = 40    
        self.offset_x = 0        
        self.offset_y = 0
        self.font = pygame.font.Font(None, 18)

        self._compute_layout()

    def _compute_layout(self):
        self.room_layout.clear()

        # Center the minimap around the start room
        start = self.dungeon.get_start_room()
        sx, sy = start.grid_pos

        for room in self.dungeon.rooms:
            gx, gy = room.grid_pos

            # shift so start room appears at (0,0)
            self.room_layout[room] = (gx - sx, gy - sy)

    def _room_screen_pos(self, surface, room):
        """Convert grid coords → screen coords INSIDE minimap box."""

        if room not in self.room_layout:
            return (0, 0)

        gx, gy = self.room_layout[room]

        # minimap box position
        map_w = 400
        map_h = 300
        map_x = surface.get_width() - map_w - 20
        map_y = 20

        # center inside minimap box
        center_x = map_x + map_w // 2
        center_y = map_y + map_h // 2

        x = center_x + gx * self.grid_spacing
        y = center_y + gy * self.grid_spacing

        return x, y

    def draw(self, surface, current_room):
        if not self.dungeon.rooms:
            return

        # ---- background rect ----
        map_w = 400
        map_h = 300
        map_x = surface.get_width() - map_w - 20
        map_y = 0
        minimap_rect = pygame.Rect(map_x, map_y, map_w, map_h)

        pygame.draw.rect(surface, (0, 0, 0), minimap_rect)
        pygame.draw.rect(surface, (80, 80, 80), minimap_rect, 2)

        # ---- draw connections ----
        for room in self.dungeon.rooms:
            if not room.visited:
                continue

            x1, y1 = self._room_screen_pos(surface, room)

            for nbr in room.neighbors:
                if not nbr.visited:
                    continue
                x2, y2 = self._room_screen_pos(surface, nbr)
                pygame.draw.line(surface, (120, 120, 120), (x1, y1), (x2, y2), 2)

        # ---- draw room nodes ----
        for room in self.dungeon.rooms:
            if not room.visited:
                continue

            x, y = self._room_screen_pos(surface, room)

            if room is current_room:
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

            label_char = room.room_type[0] if room.room_type else "N"
            label = self.font.render(label_char, True, (0, 0, 0))
            label_rect = label.get_rect(center=(x, y))
            surface.blit(label, label_rect)
