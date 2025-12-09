import random
import pygame
from Entities.projectile import Projectile

ATTACK_FUNCTIONS = {}

def attack_shoot(enemy, projectiles, dt) :
    enemy.shoot(projectiles, speed=250)

ATTACK_FUNCTIONS["shoot"] = attack_shoot

def attack_charge(enemy, projectiles, dt) :
    enemy.charge(dt, enemy.target)

ATTACK_FUNCTIONS["charge"] = attack_charge

class Enemy:

    def __init__(self, hp, speed, room, enemy_type):
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.room = room
        self.type = enemy_type
        self.alive = True

        self.position = pygame.Vector2(0,0)

        self.state = "idle"
        self.target = None

        self.action_timer = 0
        self.action_cooldown = 1.0

        self.aggro_range = 200 #px
        self.attack_range = 100 #px

        #roam functions
        self.roam_direction = pygame.Vector2(0, 0)
        self.roam_timer = 0
        self.roam_interval = random.uniform(1.0, 2.5)

    def move_with_collision(self, dx, dy, dt, speed=None):
        if speed is None:
            speed = self.speed

        # horizontal
        self.position.x += dx * speed * dt
        self.hitbox.center = (int(self.position.x), int(self.position.y))

        for wall in self.room.walls:
            if self.hitbox.colliderect(wall):
                if dx > 0:
                    self.position.x = wall.left - self.hitbox.width // 2
                else:
                    self.position.x = wall.right + self.hitbox.width // 2
                self.hitbox.center = (int(self.position.x), int(self.position.y))

        # vertical
        self.position.y += dy * speed * dt
        self.hitbox.center = (int(self.position.x), int(self.position.y))

        for wall in self.room.walls:
            if self.hitbox.colliderect(wall):
                if dy > 0:
                    self.position.y = wall.top - self.hitbox.height // 2
                else:
                    self.position.y = wall.bottom + self.hitbox.height // 2
                self.hitbox.center = (int(self.position.x), int(self.position.y))

    def update(self, dt, player, projectiles) :
        self.dt = dt
        self.target = player
        self.action_timer -= dt

        self.update_state()

        if self.state == "roaming" :
            self.roam(dt)
        
        elif self.state == "chasing" :
            self.chase(dt, player)

        elif self.state == "attacking" and self.action_timer <= 0:
            self.perform_random_action(projectiles)
            self.action_timer = self.action_cooldown

    def update_state(self) :
        distance = self.position.distance_to(self.target.position)

        if distance < self.attack_range :
            self.state = "attacking"

        elif distance < self.aggro_range :
            self.state = "chasing"

        else :
            self.state = "roaming"

    def roam(self, dt):
        self.roam_timer -= dt

        if self.roam_timer <= 0:
            angle = random.uniform(0, 360)
            self.roam_direction = pygame.Vector2(1, 0).rotate(angle)
            self.roam_interval = random.uniform(1.0, 2.5)
            self.roam_timer = self.roam_interval

        dx, dy = self.roam_direction.x, self.roam_direction.y
        self.move_with_collision(dx, dy, dt)

    def chase(self, dt, player):
        direction = (player.position - self.position)

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.move_with_collision(direction.x, direction.y, dt)
    
    def shoot(self, projectiles, speed = 250) :
        direction = (self.target.position - self.position).normalize()

        projectile = Projectile(
            position=self.position,
            ptype="Basic",
            direction=direction,
            owner=self
        )

        projectiles.append(projectile)


    def perform_random_action(self, projectiles) :
        if not hasattr(self, "attacks") or len(self.attacks) == 0:
            return
        
        action_name = random.choice(self.attacks)

        if action_name in ATTACK_FUNCTIONS :
            ATTACK_FUNCTIONS[action_name](self, projectiles, self.dt)
        else :
            print(f"[AI ERROR] Unknown action: {action_name}")
    
    def draw(self, surface):
        if hasattr(self, "sprite"):
            surface.blit(self.sprite, self.hitbox.topleft)
        else:
            # fallback debug drawing
            pygame.draw.circle(surface, (200, 50, 50), (int(self.position.x), int(self.position.y)), 16)

    def die(self) :
        self.alive = False
        
        if hasattr(self, "on_death_callback") and self.on_death_callback :
            self.on_death_callback(self)

    def take_damage(self, amount, knockback=None):
        self.hp -= amount

        if knockback is not None:
            self.knockback = pygame.Vector2(knockback)

        if self.hp <= 0:
            self.die()

BOSSES = ["Ember Lich", "Mech-ssassin", "Bone General"]

import random

class Boss(Enemy) :

    BOSS_STATS = {
        "Ember Lich" : {
            "hp": 400,
            "speed": 20,
            "attacks": ["fireball", "flame_shockwave", "meteor_drop"],
            "has_stages": True,
            "stage_thresholds":[0.5, 0.3],
            "color": (255, 165, 0),
            "sprite" : "Assets/Images/Lich Boss.png"
        },

        "Mech-ssassin" : {
            "hp": 400,
            "speed": 30,
            "attacks": ["phase", "dagger_fall", "arm_launch"],
            "has_stages": True,
            "stage_thresholds":[0.5, 0.3],
            "color": (255, 165, 0),
            "sprite" : "Assets/Images/Mech-ssassin.png"
        },

        "Bone General" : {
            "hp": 400,
            "speed": 15,
            "attacks": ["summon", "bone_rush", "flame_puddle"],
            "has_stages": True,
            "stage_thresholds":[0.5, 0.3],
            "color": (255, 165, 0),
            "sprite" : "Assets/Images/Bone General.png"
        }
    }

    def __init__(self, boss_id, room) :
        data = Boss.BOSS_STATS[boss_id]

        super().__init__(data["hp"], data["speed"], room, "Boss")

        self.name = boss_id
        self.attacks = data["attacks"]
        self.thresholds = data["stage_thresholds"]
        self.color = data["color"]

        self.current_stage = 0

        sprite_path = data["sprite"]
        self.sprite = pygame.image.load(sprite_path).convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (512, 380))

        self.rect = self.sprite.get_rect(center=(room.width//2, room.height//2))

    def update(self, dt, player, projectiles) :
        hp_ratio = self.hp / self.max_hp

        if (self.current_stage < len(self.thresholds) 
            and hp_ratio <= self.thresholds[self.current_stage]) :
            
            self.current_stage += 1
            print(f"{self.name} entered STAGE {self.current_stage + 1}!")
        
        super().update(dt, player, projectiles)

    @staticmethod
    def spawn_boss(room) :
        print("Spawning Boss...")

        valid_bosses = [
            name for name, data in Boss.BOSS_STATS.items()
            if "hp" in data
        ]
        boss_id = random.choice(valid_bosses)

        boss = Boss(boss_id, room)

        # Center boss
        boss.position = pygame.Vector2(room.width // 2, room.height // 2)
        boss.hitbox = pygame.Rect(0, 0, 96, 96)
        boss.hitbox.center = boss.position

        room.boss = boss
        return boss

    def draw(self, surface):
        self.rect.center = (int(self.position.x), int(self.position.y))
        surface.blit(self.sprite, self.rect.topleft)

import pygame
import random
from Assets.texture_manager import TextureManager
from Assets import sound_manager

class Brute(Enemy) :
    def __init__(self, room):
        super().__init__(
            hp=150,          
            speed=40,   
            room=room,
            enemy_type="Brute",
        )

        self.position = pygame.Vector2(
            random.randint(150, room.width - 150),
            random.randint(150, room.height - 150)
        )

        self.sprite = TextureManager.load(
            "Assets/Images/enemy_brute.png",
            scale=(128, 128)
        )

        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

        self.attacks = ["charge"]   
        self.attack_range = 90

        self.hitbox = pygame.Rect(0, 0, self.width, self.height)
        self.hitbox.center = self.position

        self.charge_cooldown_timer = 0.01
        self.charging = False
        self.windup_time = 0.035
        self.charge_speed = 450
        self.charge_timer = 0
        self.charge_direction = pygame.Vector2(0, 0)
        self.charge_cooldown = 0.05

        self.attack_range = 220
        self.aggro_range = 500

    def die(self) :
        super().die()
        sound_manager.brute_die.play()

    def charge(self, dt, player):

        if not self.charging and self.charge_cooldown_timer > 0:
            self.charge_cooldown_timer -= dt
            return

        # Begin windup phase
        if not self.charging and self.charge_timer <= 0:
            self.charge_direction = (player.position - self.position).normalize()
            self.charging = True
            self.charge_timer = self.windup_time
            self.action_timer = self.action_cooldown  # prevent re-attacking
            return

        # Windup counting down
        if self.charging and self.charge_timer > 0:
            self.charge_timer -= dt
            return

        # Charge movement
        if self.charging and self.charge_timer <= 0:

            dx, dy = self.charge_direction.x, self.charge_direction.y
            self.move_with_collision(dx, dy, dt, speed=self.charge_speed)

            # Stop if hit wall
            for wall in self.room.walls:
                if self.hitbox.colliderect(wall):
                    self.stop_charge()
                    return

            # Hit player
            if self.hitbox.colliderect(player.hitbox):
                player.take_damage(20, player.knockback)
                player.knockback = self.charge_direction * 400
                self.stop_charge()
                return

    def stop_charge(self) :
        self.charging = False
        self.charge_timer = 0
        self.charge_cooldown_timer = self.charge_cooldown

    def update(self, dt, player, projectiles):
        if self.charging:
            self.charge(dt, player)
            return

        super().update(dt, player, projectiles)

        self.hitbox.center = (int(self.position.x), int(self.position.y))

class Grunt(Enemy):
    def __init__(self, room):
        super().__init__(
            hp=40,
            speed=70,
            room=room,
            enemy_type="Grunt",
        )
        self.position = pygame.Vector2(
            random.randint(100, room.width - 100),
            random.randint(100, room.height - 100)
        )

        self.sprite = TextureManager.load(
            "Assets/Images/enemy_grunt.png", 
            (64, 64)
        )

        self.attacks = ["shoot"]
        self.aggro_range = 220
        self.attack_range = 140

        self.hitbox = pygame.Rect(0, 0, 24, 24)
        self.hitbox.center = (int(self.position.x), int(self.position.y))
    
    def die(self) :
        super().die()
        sound_manager.grunt_die.play()