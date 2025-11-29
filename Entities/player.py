import pygame
from Dungeon.dungeon_generator import DungeonGenerator

class Player:
    
    def __init__(self, game) :
        self.game = game

        self.hp = 100
        self.weapons = []
        self.upgrades = []
        self.consumables = []
        self.current_room = None

        self.position = pygame.Vector2(100,100)
        self.velocity = pygame.Vector2(0,0)
        self.speed = 200
        self.rect = pygame.Rect(0,0,32,32)

        self.hitbox = pygame.Rect(0,0,30,30)

        self.knockback = pygame.Vector2(0, 0)

        scaled_size = self.game.resolution.scale_value(32)
        self.size = pygame.Rect(0, 0, scaled_size, scaled_size)

    def draw(self, surface) :
        pygame.draw.rect(surface, (50, 200, 255), self.rect)
        #TODO load sprite
        #self.sprite = pygame.image.load("Assets/player.png").convert_alpha()
        #self.sprite = pygame.transform.scale(self.sprite, (32, 32))

    def spawn_at(self, room) :
        self.current_room = room
        self.position = pygame.Vector2(room.width // 2, room.height // 2)

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

    def update(self, dt, walls=None) :
        self.handle_input()

        self.position += self.velocity * self.speed * dt
        self.rect.topleft = self.position
        self.hitbox.center = self.rect.center

        # apply knockback
        if self.knockback.length_squared() > 0:
            self.position += self.knockback * dt
            self.hitbox.topleft = self.position
        
            # dampen knockback (friction)
            self.knockback *= 0.85

        self.handle_movement(dt, walls)
        self.handle_combat(dt)


    def handle_movement(self, dt, walls):
        # horizontal movement
        # horizontal movement
        self.position.x += self.velocity.x * self.speed * dt
        self.hitbox.topleft = self.position

        for wall in walls:
            if self.hitbox.colliderect(wall):
                if self.velocity.x > 0:  # moving right into wall
                    self.position.x = wall.left - self.hitbox.width
                    self.knockback.x = -300   # ← bounce left
                elif self.velocity.x < 0:  # moving left into wall
                    self.position.x = wall.right
                    self.knockback.x = 300    # ← bounce right

                self.hitbox.topleft = self.position

        # vertical movement
        self.position.y += self.velocity.y * self.speed * dt
        self.hitbox.topleft = self.position

        for wall in walls:
            if self.hitbox.colliderect(wall):
                if self.velocity.y > 0:  # moving down
                    self.position.y = wall.top - self.hitbox.height
                    self.knockback.y = -300   # bounce upward
                elif self.velocity.y < 0:  # moving up
                    self.position.y = wall.bottom
                    self.knockback.y = 300    # bounce downward

                self.hitbox.topleft = self.position

                
    def handle_combat(self, dt) :
        

    #TODO make sure enemies don't immediately attack
    def teleport_to_room(self, room) :
        self.current_room = room
        self.position = pygame.Vector2(room.spawn_point)
        print("Teleported to", room)