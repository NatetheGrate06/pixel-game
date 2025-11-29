import pygame

class Weapon:
    #TODO
    def __init__(self, name, cooldown) :
        self.name = name
        self.cooldown = cooldown
        self.cooldown_timer = 0
        self.game = None

    
class Gun(Weapon):
    def __init__(self, damage, speed):
        super().__init__("Gun", cooldown=0.2)
        self.damage = damage
        self.projectile_speed = speed

    def attack(self, direction):
        from Entities.projectile import Projectile

        player = self.game.player
        start_pos = pygame.Vector2(player.hitbox.center)

        proj = Projectile(
            position=start_pos,
            ptype="Basic",   
            direction=direction,     
            owner=player
        )

        player.game.projectiles.append(proj)
        print("Pew!")



class Melee(Weapon) :
    def __init__(self, damage, range_) :
        super().__init__(name="Melee", cooldown=0.4)
        self.damage = damage
        self.range = range_

    def attack(self, direction) :
        player = self.game.player
        center = pygame.Vector2(player.hitbox.center)

        hitbox = pygame.Rect(0, 0, self.range, self.range)
        hitbox.center = (center + direction * (self.range * 0.6))

        for enemy in self.game.enemies :
            if hitbox.colliderect(enemy.hitbox) :
                enemy.take_damage(self.damage)
                enemy.knockback = direction * 200

        print("Slash!")