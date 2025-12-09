import pygame
from Dungeon.dungeon_generator import DungeonGenerator
from Entities.weapon import Weapon, Melee
from Assets import sound_manager

class Player:
    
    def __init__(self, game) :
        self.game = game

        self.hp = 100
        self.weapons = []
        self.upgrades = []
        self.consumables = []
        self.current_room = None
        self.alive = True

        self.position = pygame.Vector2(100,100)
        self.velocity = pygame.Vector2(0,0)
        self.speed = 200
        self.rect = pygame.Rect(0,0,32,32)

        self.hitbox = pygame.Rect(0,0,30,30)

        self.knockback = pygame.Vector2(0, 0)

        scaled_size = self.game.resolution.scale_value(32)
        self.size = pygame.Rect(0, 0, scaled_size, scaled_size)

        self.active_weapon_index = 0

        self.sprite = pygame.image.load("Assets/Images/mc-bios.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))

        self.sprite_list = [self.sprite]

    def draw(self, surface) :
        surface.blit(self.sprite, self.hitbox.topleft)

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
        self.handle_combat(dt)

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

    def get_attack_direction(self) :
        # Cursor world position is just screen position for now 
        mouse_x, mouse_y = pygame.mouse.get_pos()

        player_center = pygame.Vector2(self.hitbox.center)

        direction = pygame.Vector2(mouse_x, mouse_y) - player_center

        if direction.length_squared() == 0:
            return pygame.Vector2(0, -1)

        return direction.normalize()

    def handle_combat(self, dt) :
        if not self.weapons :
            return
        
        weapon = self.weapons[self.active_weapon_index]
        if weapon.cooldown_timer > 0 :
            weapon.cooldown_timer -= dt

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and weapon.cooldown_timer <= 0 :
            direction = self.get_attack_direction()
            weapon.attack(direction)

            if isinstance(weapon, Melee):
                sound_manager.slash.play()
            else:
                sound_manager.shoot.play()

            weapon.cooldown_timer = weapon.cooldown

        if key[pygame.K_x] :
            if not hasattr(self, "_switch_cooldown") :
                self._switch_cooldown = 0

            if self._switch_cooldown <= 0:
                if len(self.weapons) > 1:
                    self.active_weapon_index = 1 - self.active_weapon_index
                self._switch_cooldown = 0.25
            
            if hasattr(self, "_switch_cooldown") and self._switch_cooldown > 0 :
                self._switch_cooldown -= dt
                

    def handle_movement(self, dt, walls):
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

    def teleport_to_room(self, room) :
        self.current_room = room
        self.position = pygame.Vector2(room.spawn_point)
        print("Teleported to", room)

    def die(self) :
        self.alive = False
        sound_manager.player_die.play()

    def take_damage(self, damage, knockback) :
        self.hp -= damage

        if knockback is not None:
            self.knockback = pygame.Vector2(knockback)

        if self.hp <= 0:
            self.die()

    def equip_weapon(self, weapon) :
        weapon.game = self.game
        if len(self.weapons) < 2 :
            self.weapons.append(weapon)
        else :
            print("Gun capacity reached.")
            return