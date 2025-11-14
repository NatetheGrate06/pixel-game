class Room: 
    def __init__(self, is_start=False, is_boss=False) :
        self.is_start = is_start
        self.is_boss = is_boss
        
        self.enemies = []
        self.loot = []

        def enter(self):
            #TODO combat logic
            pass

        def update(self, dt) :
            for enemy in self.enemies:
                enemy.update(dt)