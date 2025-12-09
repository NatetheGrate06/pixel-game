from UI.ui_manager import UIManager
from UI.menu_button import MenuButton
import os

import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Menu :

    def __init__(self, screen, state_manager, game) :
        self.screen = screen
        self.state_manager = state_manager
        self.game = game

        self.font = pygame.font.Font(None, 80)

        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "..", "Assets", "Images", "menu_background.webp")
        path = os.path.normpath(path)

        print("Loading background:", path)
        self.background = pygame.image.load(path).convert_alpha()

        # scale
        self.background = pygame.transform.scale(
            self.background,
            (screen.get_width(), screen.get_height())
        )
        button_dir = os.path.join(base, "..", "Assets", "Images")

        self.buttons = [
            MenuButton(os.path.join(button_dir, "play.png"), 
                    (screen.get_width() // 2, 400), 
                    "Start Game"),

            MenuButton(os.path.join(button_dir, "settings.png"),
                    (screen.get_width() // 2, 520),
                    "Settings"),

            MenuButton(os.path.join(button_dir, "credits.png"),
                    (screen.get_width() // 2, 640),
                    "Credits"),

            MenuButton(os.path.join(button_dir, "quit.png"),
                    (screen.get_width() // 2, 760),
                    "Quit"),
        ]

        title_path = os.path.join(base, "..", "Assets", "Images", "title.png")
        self.title_image = pygame.image.load(title_path).convert_alpha()

        # resize or leave as-is
        tw, th = self.title_image.get_size()
        self.title_image = pygame.transform.scale(self.title_image, (tw * 5, th * 5))

        self.title_pos = self.title_image.get_rect(center=(screen.get_width() // 2, 150))

        self.title_pos = (screen.get_width() // 2 - self.title_image.get_width() // 2, 0)


    def update(self, events) :
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_hovered() :
                        self.button_action(button.action)

    def button_action(self, text) :

        match text :
            case "Start Game" :
                self.state_manager.change_state("GAME")
                self.game.start_game()
            case "Settings" :
                self.state_manager.change_state("SETTINGS")
            case "Credits" :
                self.state_manager.change_state("CREDITS")
            case "Quit" :
                pygame.quit()
                exit()

    def draw(self) :
        self.screen.blit(self.background, (0,0))

        self.screen.blit(self.title_image, self.title_pos)

        for button in self.buttons:
            button.draw(self.screen)

        