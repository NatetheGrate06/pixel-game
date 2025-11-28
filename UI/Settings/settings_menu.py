import pygame

RESOLUTIONS = [
    (1280, 720),
    (1600, 900),
    (1920, 1080),
    (2560, 1440),
    ("Fullscreen")
]

class SettingsMenu :
    
    def apply_screen_setting(self, choice):
        if choice == "Fullscreen":
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            width, height = pygame.display.get_surface().get_size()
            self.resolution.apply_resolution(width, height)
        else:
            width, height = choice
            pygame.display.set_mode((width, height), pygame.RESIZABLE)
            self.resolution.apply_resolution(width, height)
