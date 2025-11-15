from UI.ui_manager import UIManager
from UI.menu_button import MenuButton
import os

import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Menu :

    def __init__(self, screen, state_manager) :
        self.screen = screen
        self.state_manager = state_manager

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
        self.buttons = [
            MenuButton("Start Game", (screen.get_width() // 2, 300)),
            MenuButton("Settings", (screen.get_width() // 2, 380)),
            MenuButton("Credits", (screen.get_width() // 2, 460)),
            MenuButton("Quit", (screen.get_width() // 2, 540)),
        ]

        self.title_text = self.font.render("BIOS4096", True, (255, 255, 255))
        self.title_pos = (screen.get_width() // 2 - self.title_text.get_width() // 2, 100)


    def update(self, events) :
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_hovered() :
                        self.button_action(button.text)

    def button_action(self, text) :

        match text :
            case "Start Game" :
                self.state_manager.change_state("GAME")
            case "Settings" :
                self.state_manager.change_state("SETTINGS")
            case "Credits" :
                self.state_manager.change_state("CREDITS")
            case "Quit" :
                pygame.quit()
                exit()

    def draw(self) :
        self.screen.blit(self.background, (0,0))

        self.screen.blit(self.title_text, self.title_pos)

        for button in self.buttons:
            button.draw(self.screen)

        