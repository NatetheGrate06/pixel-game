class Weapon:
    #TODO
    def __init__(self, name, cooldown) :
        self.name = name
        self.cooldown = cooldown
        self.cooldown_timer = 0

    def attack(self, direction) :
        raise NotImplementedError