from Dungeon.room import Room
import random

class DungeonGenerator:
    def __init__(self, width=10, height=10) :
        self.width = width
        self.height = height
        self.rooms = []

    def generate_new_floor(self):
        self.rooms = []
        self._generate_rooms()
        self._connect_rooms()
        self._place_entities()

    def _generate_rooms(self) :
        #TODO optimize with tree implementation
        for i in range(25) :
            if Room().is_start == True :
                self.rooms[0].equals(Room())
            else :
                self.rooms.append(Room())

    def _connect_rooms(self) :
        pass #TODO create graph of rooms

    def _place_entities(self) :
        pass #TODO

    def get_start_room(self) :
        #TODO
        return self.rooms[0] if self.rooms else None
    
    def update(self, dt) :
        for room in self.rooms:
            room.update(dt)

    def get_random_room(self, exclude=None) :
        choices = [room for room in self.rooms if room is not exclude]

        if not choices: 
            return None
        
        return random.choice(choices)
    