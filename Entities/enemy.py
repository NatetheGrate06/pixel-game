import random
import pygame
from Entities.projectile import Projectile

ATTACK_FUNCTIONS = {

}

class Enemy:

    def __init__(self, hp, speed, room, enemy_type):
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.room = room
        self.type = enemy_type

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

        self.position += self.roam_direction * self.speed * dt

        if hasattr(self, "hitbox"):
            self.hitbox.center = (int(self.position.x), int(self.position.y))

    def chase(self, dt, player) :
        direction = (player.position - self.position).normalize()
        self.position += direction * self.speed * dt
        self.hitbox.center = (int(self.position.x), int(self.position.y))
    
    def shoot(self, projectiles, speed = 250) :
        direction = (self.target.position - self.position).normalize()

        projectile = Projectile(
            position=self.position,
            ptype="Basic",
            direction=direction,
            owner=self
        )

        projectiles.append(projectile)

    def attack_shoot(enemy, projectiles, DT) :
        enemy.shoot(projectiles, speed=250)

    ATTACK_FUNCTIONS["shoot"] = attack_shoot

    def perform_random_action(self, projectiles) :
        if not hasattr(self, "attacks") or len(self.attacks) == 0:
            return
        
        action_name = random.choice(self.attacks)

        if action_name in ATTACK_FUNCTIONS :
            ATTACK_FUNCTIONS[action_name](self, projectiles, self.dt)
        else :
            print(f"[AI ERROR] Unknown action: {action_name}")
    
    def draw(self, surface) :
        if (self.type == "Brute"):
            pygame.draw.circle(surface, (200, 50, 50), (int(self.position.x), int(self.position.y)), 24)
        else :
            pygame.draw.circle(surface, (200, 50, 50), (int(self.position.x), int(self.position.y)), 12)

class Boss(Enemy) :

    BOSS_STATS = {
        "Sprinter" : {
            "hp": 300,
            "speed": 9,
            "attacks": ["dash", "triple_dash", "clone_dash"],
            "has_stages": True,
            "stage_thresholds":[0.7, 0.4],
            "color": (255, 0, 0)
        },

        "Ember Lich" : {
            "hp": 400,
            "speed": 6.5,
            "attacks": ["fireball", "flame_shockwave", "meteor_drop"],
            "has_stages": True,
            "stage_thresholds":[0.5, 0.3],
            "color": (255, 165, 0)
        },

        "Serpent" : {
            "hp": 450,
            "speed": 7.3,
            "attacks": ["burrow", "venom", "tail_swipe"],
            "has_stages": True,
            #TODO implement thresholds; pain in the butt
            "stage_thresholds":[0.8],
            "color": (0, 128, 128)
        },

        "Gear Titan" : {
            "hp": 450,
            "speed": 5,
            "attacks": ["arm_slam", "rocket_volley", "laser_sweep"],
            "has_stages": True,
            #TODO implement thresholds; pain in the butt
            "stage_thresholds":[0.8],
            "color": (128, 128, 128)
        },

        "Plague" : {

        },

        "Executioner" : {

        },

        "Priestess" : {

        },

        #Might not keep this one
        "Herald" : {

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

    def update(self, dt, player) :
        hp_ratio = self.hp / self.max_hp

        if (self.current_stage < len(self.thresholds) 
            and hp_ratio <= self.thresholds[self.current_stage]) :
            
            self.current_stage += 1
            print(f"{self.name} entered STAGE {self.current_stage + 1}!")
        
        super().update(dt, player)

import pygame
import random

class Brute(Enemy) :
    def __init__(self, room):
        super().__init__(
            hp=150,          
            speed=40,   
            room=room,
            enemy_type="Brute"
        )
        self.position = pygame.Vector2(
            random.randint(150, room.width - 150),
            random.randint(150, room.height - 150)
        )
        self.attacks = ["charge"]   
        self.attack_range = 90

        self.hitbox = pygame.Rect(0, 0, 32, 32)
        self.hitbox.center = (int(self.position.x), int(self.position.y))

        self.charge_cooldown_timer = 0.01
        self.charging = False
        self.windup_time = 0.035
        self.charge_speed = 450
        self.charge_timer = 0
        self.charge_direction = pygame.Vector2(0, 0)
        self.charge_cooldown = 0.05

        self.attack_range = 220
        self.aggro_range = 500

    def charge(self, dt, player):
        print("ENTERED CHARGE FUNCTION, TIMER:", self.charge_cooldown_timer)

        if self.charge_cooldown_timer > 0:
            print("Cooldown")
            self.charge_cooldown_timer -= dt
            return

        if not self.charging and self.charge_timer <= 0:
            print("Start windup")
            self.charge_direction = (player.position - self.position).normalize()
            self.charging = True
            self.charge_timer = self.windup_time
            return

        if self.charging and self.charge_timer > 0:
            print("Winding up")
            self.charge_timer -= dt
            if self.charge_timer <= 0 :
                self.charge_timer = 0
            return

        if self.charging and self.charge_timer <= 0:
            print("Charge")
            movement = self.charge_direction * self.charge_speed * dt
            self.position += movement

            self.hitbox.center = (int(self.position.x), int(self.position.y))

            #for wall in self.room.walls:
             #   if self.hitbox.colliderect(wall):
              #      self.stop_charge()
               #     return

            if self.hitbox.colliderect(player.hitbox):
                if hasattr(player, "take_damage"):
                    player.take_damage(20)
                player.knockback = self.charge_direction * 400
                self.stop_charge()
                return

            
    def stop_charge(self) :
        self.charging = False
        self.charge_timer = 0
        self.charge_cooldown_timer = self.charge_cooldown

    def attack_charge(enemy, projectiles, dt) :
        enemy.charge(dt, enemy.target)

    ATTACK_FUNCTIONS["charge"] = attack_charge

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
            enemy_type="Grunt"
        )
        self.position = pygame.Vector2(
            random.randint(100, room.width - 100),
            random.randint(100, room.height - 100)
        )
        self.attacks = ["shoot"]
        self.aggro_range = 220
        self.attack_range = 140

        self.hitbox = pygame.Rect(0, 0, 24, 24)
        self.hitbox.center = (int(self.position.x), int(self.position.y))