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

        self.hitbox = pygame.Rect(0,0,30,30)

    def draw(self, surface) :
        pygame.draw.rect(surface, (50, 200, 255), self.size)
        #TODO load sprite
        #self.sprite = pygame.image.load("Assets/player.png").convert_alpha()
        #self.sprite = pygame.transform.scale(self.sprite, (32, 32))

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

    def update(self, dt, walls=None) :
        self.handle_input()

        self.position += self.velocity * self.speed * dt
        self.size.topleft = self.position

        self.handle_movement(dt, walls)
        self.handle_combat(dt)


    def handle_movement(self, dt, walls=None) :
        self.velocity = self.velocity.lerp(pygame.Vector2(0, 0), 0.2)
        self.position.x += self.velocity.x * self.speed * dt
        self.hitbox.topleft = self.position

        if not walls: 
            return

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

    #TODO make sure enemies don't immediately attack
    def teleport_to_room(self, room) :
        self.current_room = room
        self.position = room.spawn_point
        print("Teleported to", room)