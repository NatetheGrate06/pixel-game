import pygame

class UIManager :

    def __init__(self, player) :
        self.player = player

        self.health_bar = HealthBar(player) 
        self.ammo_counter = AmmoCounter(player)
        self.upgrade_inv = Upgrade(player)
        self.consumable_inv = Consumable(player)

        self.boss_bar = None
        self.floating_texts = FloatingTextManager()

    def set_boss(self, boss) :
        self.boss_bar = BossHealthBar(boss)

    def update(self, dt) :
        if self.boss_bar:
            self.boss_bar.update(dt)
        self.floating_texts.update(dt)

    def draw(self, surface) :
        self.health_bar.draw(surface)
        self.ammon_counter.draw(surface)

        if self.boss_bar :
            self.boss_bar.draw(surface)
        
        self.floating_texts.draw(surface)

class HealthBar :

    def __init__(self, player) :
        self.player = player
        self.width = 200
        self.height = 20
        self.position = pygame.Vector2(20,20)

    def draw(self, surface) :
        RED = (200, 0, 0)

        hp_ratio = self.player.hp / self.player.max_hp

        pygame.draw.rect(surface, RED), (self.position[0], self.position[1], self.width * hp_ratio, self.height)

class AmmoCounter :

    def __init__(self, player) :
        self.player = player
        self.font = pygame.font.Font(None, 32)
        self.position = (20, 50)

    def draw(self, surface) :
        ammo_text = f"Ammo: {self.player.weapon.ammo}/{self.player.weapon.max_ammo}"
        img = self.font.render(ammo_text, True, (255, 255, 255))
        surface.blit(img, self.position)

class BossHealthBar :

    def __init__(self, boss) :
        self.boss = boss
        self.width = 400
        self.height = 25
        self.position = (100, 30)
    
    def update(self, dt) :
        #TODO animations
        pass

    def draw(self, surface) :
        hp_ratio = self.boss.hp / self.boss.max_hp

        #background
        pygame.draw.rect(surface, (30,0,0), (*self.position, self.width, self.height))

        #filled bar
        pygame.draw.rect(surface, (200, 20, 20), (self.position[0], self.position[1], self.width * hp_ratio, self.height))

        #boss name
        font = pygame.font.Font(None, 28) 
        name_text = font.render(self.boss.name, True, (255, 255, 255))
        surface.blit(name_text, (self.position[0], self.position[1] - 20))

class FloatingText:

    def __init__(self, text, position, color=(255, 255, 255)) :
        self.text = text
        self.position = pygame.Vector2(position)
        self.color = color
        self.timer = 1.0
        self.font = pygame.font.Font(None, 24)

    def update(self, dt) :
        self.timer -= dt
        self.pos.y -= 40 * dt #float upward

    def draw(self, surface) :
        if self.timer > 0:
            img = self.font.render(self.text, True, self.color)
            surface.blit(img, self.pos)

class FloatingTextManager:
    #TODO will implement priority queue for text
    def __init__(self):
        self.texts = []

    def add(self, text, position, color=(255, 255, 255)):
        self.texts.append(FloatingText(text, position, color))

    def update(self, dt):
        for t in self.texts[:]:
            t.update(dt)
            if t.timer <= 0:
                self.texts.remove(t)

    def draw(self, surface):
        for t in self.texts:
            t.draw(surface)

class Upgrade :

    def __init__(self, player) :
        self.player = player
        self.width = 180
        self.height = 60
        self.position = pygame.Vector2(20, 100)
        self.font = pygame.font.Font(None, 28)

    def draw(self, surface) :
        for i in range(len(Upgrade.upgrades)) :
            pygame.draw.rect(surface, (255, 255, 255), (self.position[0] * i + 40, self.position[1], self.width / len(Upgrade.upgrades), self.height))

            upgrade_name = Upgrade.upgrades[i].get_upgrade()
            img = self.font.render(upgrade_name, True, (255, 255, 255))
            surface.blit(img, (self.postion[0] + (60 * i), self.position[1]))

    def update(self, dt) :
        #TODO animations
        pass

from Items.consumable import Consumable

class Consumables :
    #TODO regular queue implementation for consumables
    def __init__(self, player) :
        self.player = player
        self.width = 180
        self.height = 60
        self.position = pygame.Vector2(100, 100)
        self.font = pygame.font.Font(None, 28)

    def draw(self, surface) :
        for i in range(len(Consumable.consumables)) :
            pygame.draw.rect(surface, (255, 255, 255), (self.position[0] * i + 40, self.position[1], self.width / len(Consumable.consumables), self.height))

            consumable_name = Consumable.consumables[i].get_consumables()
            img = self.font.render(consumable_name, True, (255, 255, 255))
            surface.blit(img, (self.postion[0] + (60 * i), self.position[1]))

    def update(self, dt) :
        #TODO animations
        pass 