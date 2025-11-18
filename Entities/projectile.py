from Entities.weapon import Weapon
import pygame

#TODO add trails, bullet spread, sprite projectiles
TYPES = {
    "Ricochet" : {
        "speed" : 8,
        "damage" : 5,
        "life" : 5
    }, 

    "Flame" : {
        "speed" : 6.5,
        "damage" : 3,
        "life" : None
    },

    "Homing" : {
        "speed" : 4,
        "damage" : 20,
        "life" : 5
    },

    "Spread" : {
        "speed": 10,
        "damage": 5,
        "life" : None
    },

    "Piercing" : {
        "speed" : 8,
        "damage" : 7,
        "life" : 5
    }
}

class Projectile :
    def __init__(self, position, type, speed, direction, damage, owner=None, radius=4, color=(255,255,255)) :
        data = TYPES[type]

        self.type = type
        self.speed = speed
        self.pos = pygame.Vector2(position)
        self.dir = pygame.Vector2(direction).normalize()
        self.damage = damage
        self.owner = owner

        self.radius = radius
        self.color = color

        self.rect = pygame.Rect(self.pos.x, self.pos.y, radius*2, radius*2)

        self.lifespan = data.get("life")


    def update(self, dt, walls, enemies) :
        
        #make sure projectile exists
        if not self.alive:
            return

        self.pos += self.dir * self.speed * dt
        self.rect.center = self.pos

        self.age += dt
        if self.age >= self.lifespan:
            self.alive = False
            return
        
        for wall in walls:
            if self.rect.colliderect(wall) and self.type != TYPES["Ricochet"]:
                self.alive = False
                return
            
        for enemy in enemies: 
            if enemy is not self.owner and self.rect.colliderect(enemy.hitbox):
                enemy.take_damage(self.damage)
                self.alive = False
                return
            
    def draw(self, surface) :
        if self.alive:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

class Cursor:
    def __init__(self) :
        pygame.mouse.set_visible(False)
        self.position = pygame.mouse.get_pos()
        self.color = (255, 255, 255)
        self.radius = 6

    def update(self) :
        self.position = pygame.mouse.get_pos()

    def draw(self, surface) :
        pygame.draw.circle(surface, self.color, self.position, self.radius, 2) 