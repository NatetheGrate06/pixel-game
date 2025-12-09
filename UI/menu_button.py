import pygame
import os

class MenuButton:
    def __init__(self, image_path, center_pos, action_name):
        """
        image_path  – path to the button texture
        center_pos  – (x, y) where the button is centered
        action_name – "Start Game", "Settings", etc.
        """
        self.action = action_name

        # Load sprite
        self.image = pygame.image.load(image_path).convert_alpha()

        # Optionally scale it
        scale = 2.5
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w * scale), int(h * scale)))

        self.rect = self.image.get_rect(center=center_pos)

        # Hover effect
        self.hover_image = self.image.copy()
        self.hover_image.fill((50, 50, 50, 0), special_flags=pygame.BLEND_RGB_ADD)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        if self.is_hovered():
            surface.blit(self.hover_image, self.rect)
        else:
            surface.blit(self.image, self.rect)
