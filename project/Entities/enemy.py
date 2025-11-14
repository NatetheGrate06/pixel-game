class Enemy:
    def __init__(self, hp, speed, room, type):
        self.hp = hp
        self.speed = speed
        self.room = room
        self.type = type
        self.position = (0,0)

    def update(self, dt) :
        self.move(dt)
        self.act(dt)

    def move(self, dt) :
        raise NotImplementedError
    
    def move(self, dt) :
        raise NotImplementedError
    
class Boss(Enemy) :

    def __init__(self, has_stages, num_stages, **kwargs) :
        super().__init__(hp=500, speed=get_boss_speed(self.type), room="Boss Room", type="Boss")
        self.has_stages = False
        self.num_stages = num_stages

    BOSS_STATS = {
        "Sprinter" : {
            "hp": 300,
            "speed": 9,
            "attacks": ["dash", "triple_dash", "clone_dash"],
            "has_stages": True,
            "stage_thresholds":[0.7, 0.4],
            "color": (255, 0, 0)
        },

        "Ember" : {

        },

        "Serpent" : {

        },

        "Gear Titan" : {

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