from Entities.weapon import Weapon
import pygame

#TODO add trails, bullet spread, sprite projectiles
TYPES = {
    "Ricochet" : {
        "speed" : 800,
        "damage" : 5,
        "life" : 5
    }, 

    "Flame" : {
        "speed" : 650,
        "damage" : 3,
        "life" : None
    },

    "Homing" : {
        "speed" : 400,
        "damage" : 20,
        "life" : 5
    },

    "Spread" : {
        "speed": 1000,
        "damage": 5,
        "life" : None
    },

    "Piercing" : {
        "speed" : 800,
        "damage" : 7,
        "life" : 5
    },

    "Basic" : {
        "speed" : 500,
        "damage" : 5,
        "life" : 5
    }
}

class Projectile:
    def __init__(self, position, ptype, direction, owner=None, radius=4, color=(255,255,255)):
        data = TYPES[ptype]

        self.type = ptype
        self.speed = data["speed"]
        self.damage = data["damage"]
        self.lifespan = data["life"]
        self.owner = owner

        self.pos = pygame.Vector2(position)
        self.dir = pygame.Vector2(direction).normalize()

        self.radius = radius
        self.color = color

        self.rect = pygame.Rect(self.pos.x, self.pos.y, radius*2, radius*2)

        self.age = 0.0
        self.alive = True


    def update(self, dt, walls, enemies, player=None):

        if not self.alive:
            return

        # Movement
        self.pos += self.dir * self.speed * dt
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Lifespan expiration
        self.age += dt
        if self.lifespan is not None and self.age >= self.lifespan:
            self.alive = False
            return

        # Wall collision
        for wall in walls:
            if self.rect.colliderect(wall):
                if self.type == "Ricochet":
                    self.dir.x *= -1 
                    self.dir.y *= -1
                else:
                    self.alive = False
                return

        # Enemy collision
        for enemy in enemies:
            if enemy is self.owner:
                continue
            if enemy.hitbox.colliderect(self.rect):
                enemy.take_damage(self.damage)
                self.alive = False
                return
            
        if player and self.owner != player:
            if player.hitbox.colliderect(self.rect) :
                player.take_damage(self.damage, knockback=1)
                self.alive = False
                return


    def draw(self, surface):
        if self.alive:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

class Cursor:
    def __init__(self, game) :
        self.position = pygame.mouse.get_pos()
        self.color = (255, 255, 255)
        self.radius = 6
        self.game = game

        cursor_size = self.game.resolution.scale_value(16)

    def update(self) :
        self.position = pygame.mouse.get_pos()

    def draw(self, surface) :
        pygame.draw.circle(surface, self.color, self.position, self.radius, 2) 