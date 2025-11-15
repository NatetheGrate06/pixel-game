import pygame

class MenuButton :
    def __init__(self, text, center_pos) :
        self.text = text
        self.font = pygame.font.Font(None, 50)

        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.rect = self.text_surface.get_rect(center=center_pos)

        self.default_color = (255, 255, 255)
        self.hover_color = (200, 200, 200)

    def is_hovered(self) :
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface) :
        color = self.hover_color if self.is_hovered() else self.default_color

        self.text_surface = self.font.render(self.text, True, color)
        surface.blit(self.text_surface, self.rect)