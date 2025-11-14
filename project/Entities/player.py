from Entities.weapon import Weapon

class Player:
    def __init__(self) :
        self.hp = 100
        self.weapons = []
        self.upgrades = []
        self.consumables = []
        self.position = (0,0)
        self.current_room = None

    def spawn_at(self, room) :
        self.current_room = room
        self.position = (room.get_width() // 2, room.get_height() // 2)

    def update(self, dt) :
        self.handle_movement(dt)
        self.handle_combat(dt)

    def handle_movement(self, dt) :
        pass #TODO WASD movement + speed (possible dash mechanic)

    def handle_combat(self, dt) :
        pass #TODO shooting/melee

    def apply_upgade(self, upgrade) :
        #TODO keep track of upgrades in queue
        self.upgrades.append(upgrade)
        upgrade.apply(self)