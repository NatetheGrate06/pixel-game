import random
import pygame

locked_on = False
actions = []

ATTACK_FUNCTIONS = {

}

class Enemy:

    def __init__(self, hp, speed, room, type):
        self.hp = hp
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

    def update(self, dt, player) :
        self.target = player
        self.action_timer -= dt

        self.update_state()

        if self.state == "roaming" :
            self.roam(dt)
        
        elif self.state == "chasing" :
            self.chase(dt, player)

        elif self.state == ""

    def move(self, dt) :
        raise NotImplementedError
    
    def act(self, dt, action) :
        if (self.locked_on) :
            action = random.choice(self.actions)
            self.perform_action(action)

    def roam(self, dt) :
        direction = pygame.Vector2(
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ).normalize()

        self.position += direction * self.speed * dt

    def chase(self, dt, player) :
        direction = (player.position - self.position).normalize()
        self.position += direction * self.speed * dt
    


    def perform_action(self, action_name) :
        attack_func = ATTACK_FUNCTIONS[action_name]
        attack_func(self)


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

    def __init__(self, boss_id, has_stages, thresholds, color, **kwargs) :
        data = Boss.BOSS_STATS[boss_id]

        self.name = boss_id
        self.hp = data.get("hp")
        self.speed = data.get("speed")
        self.attacks = data.get("attacks")
        self.thresholds = data.get("thresholds",[])
        self.color = data.get("color")
        self.has_stages = data.get("has_stages", False)

        self.locked_on = True
        self.action_timer = 0
        self.action_cooldown = 1.0

    def update(self, dt) :
        self.action_timer -= dt
        if self.action_timer <= 0:
            self.act(dt)
            self.action_timer = self.action_cooldown

        
