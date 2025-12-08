import pygame

class Upgrade :
    def __init__(self, name, description, icon_path, apply_func) :
        self.name = name
        self.description = description 
        self.icon_path = icon_path
        self.icon = None
        self.apply = apply_func
        self.rect = None
    
    def upgrade_speed(player) :
        player.speed += 50

    def upgrade_damage(player) :
        for w in player.weapons:
            if hasattr(w, "damage") :
                w.damage += 5

            if hasattr(w, "bullet_color") :
                w.bullet_color = (255, 0, 0)

    def load_icons() :
        ICON_SIZE = 48

        for up in UPGRADES:
            if up.icon is None:
                img = pygame.image.load(up.icon_path).convert_alpha()
                img = pygame.transform.scale(img, (ICON_SIZE, ICON_SIZE))
                up.icon = img
                up.rect = img.get_rect()
                print("Loaded:", up.name)

UPGRADES = [
    Upgrade("Boots of Speed", "Move faster", "Assets/Images/upgrade_speed.jpg", Upgrade.upgrade_speed),
    Upgrade("Sharpened Bullet", "Increase gun damage","Assets/Images/upgrade_bullet.jpg", Upgrade.upgrade_damage)
]
