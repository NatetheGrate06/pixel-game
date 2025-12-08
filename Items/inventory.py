import pygame

class Inventory:
    def __init__(self):
        self.upgrades = []

    def add_upgrade(self, upgrade) :
        self.upgrades.append(upgrade)

    def draw(self, surface) :
        if not self.upgrades:
            return

        screen_w = surface.get_width()
        screen_h = surface.get_height()

        slot_size = 48
        padding = 10

        total_slots = len(self.upgrades)
        total_width = total_slots * slot_size + (total_slots - 1) * padding

        # Bottom-center origin
        start_x = (screen_w - total_width) // 2
        y = screen_h - slot_size - 20  # 20px above bottom

        for i, upgrade in enumerate(self.upgrades):
            x = start_x + i * (slot_size + padding)

            # Draw slot background
            pygame.draw.rect(surface, (50, 50, 50), (x, y, slot_size, slot_size), border_radius=6)
            pygame.draw.rect(surface, (200, 200, 200), (x, y, slot_size, slot_size), 2, border_radius=6)

            if upgrade.icon:
                surface.blit(upgrade.icon, (x, y))