class Weapon:
    #TODO
    def __init__(self, name, cooldown) :
        self.name = name
        self.cooldown = cooldown
        self.cooldown_timer = 0
        self.type = None

    def attack(self, direction) :
        raise NotImplementedError
    
class Gun(Weapon) :
    def __init__(self, damage, speed, **kwargs) :
        super().__init__(name="Gun", cooldown=0.2)
        self.damage = damage
        self.projectile_speed = speed

    def attack(self, direction) :
        print("Pew!")

class Melee(Weapon) :
    def __init__(self, damage, range_, **kwargs) :
        super().__init__(name="Melee", cooldown=0.4)
        self.damage = damage
        self.range = range_

    def attack(self, direction) :
        print("Slash!")