from Entities.weapon import Weapon
import pygame

class Player:
    def __init__(self) :
        self.hp = 100
        self.weapons = []
        self.upgrades = []
        self.consumables = []
        self.current_room = None

        self.position = pygame.Vector2(100,100)
        self.velocity = pygame.Vector2(0,0)
        self.speed = 200
        self.size = pygame.Rect(0,0,32,32)

    def spawn_at(self, room) :
        self.current_room = room
        self.position = (room.get_width() // 2, room.get_height() // 2)

    def handle_input(self) :
        keys = pygame.key.get_pressed()
        
        self.velocity.x = 0
        self.velocity.y = 0

        if keys[pygame.K_w]:
            self.velocity.y = -1
        if keys[pygame.K_s]:
            self.velocity.y = 1
        if keys[pygame.K_a]:
            self.velocity.x = -1
        if keys[pygame.K_d]:
            self.velocity.x = 1

            if self.velocity.length() != 0:
                self.velocity = self.velocity.normalize()

    def update(self, dt, walls) :
        self.handle_input()

        self.position += self.velocity * self.speed * dt
        self.size.topleft = self.position

        self.handle_movement(dt, walls)
        self.handle_combat(dt)


    def handle_movement(self, dt, walls) :
        self.position.x += self.velocity.x * self.speed * dt
        self.hitbox.topleft = self.position
        #x-axis
        for wall in walls:
            if self.hitbox.colliderect(wall) :
                #moving in left dir
                if self.velocity.x > 0:
                    self.position.x = wall.left - self.hitbox.width

                #moving in right dir
                elif self.velocity.x < 0:
                    self.position.x = wall.right

                self.hitbox.topleft = self.position
        #y-axis
        self.position.y += self.velocity.y * self.speed * dt
        self.hitbox.topleft = self.position

        for wall in walls :
             if self.hitbox.colliderect(wall) :
                #moving up
                if self.velocity.y > 0:
                    self.position.y = wall.top - self.hitbox.width

                #moving down
                elif self.velocity.y < 0:
                    self.position.y = wall.bottom

                self.hitbox.topleft = self.position

        
    def handle_combat(self, dt) :
        pass #TODO shooting/melee

    def apply_upgade(self, upgrade) :
        #TODO keep track of upgrades in queue
        self.upgrades.append(upgrade)
        upgrade.apply(self)

    def consume(self, consumeable) :
        self.consumables.append(consumeable)
        consumeable.apply(self)