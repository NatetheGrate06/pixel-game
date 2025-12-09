import pygame

class CreditsMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.resolution = game.resolution

        self.font_title = pygame.font.Font(None, 90)
        self.font_normal = pygame.font.Font(None, 48)

        # Credits text list
        self.credits = [
            "BIOS4096",
            "",
            "Created By:",
            "Nathan Vaughn",
            "",
            "Programming:",
            "Nathan Vaughn",
            "",
            "Art Assets:",
            "Taylor Douglas",
            "Nathan Vaughn",
            "",
            "Dungeon Tileset - Anon Itch.io User",
            "",
            "Music & Audio:",
            "Dylan Vaughn",
            "",
            "",
            "Thank you for playing!",
        ]

        # Scroll position
        self.scroll_y = self.game.screen.get_height() + 50
        self.scroll_speed = 40

    def update(self, dt, events):
        # Scroll upwards
        self.scroll_y -= self.scroll_speed * dt

        # Reset scroll at the end
        max_height = len(self.credits) * 60
        if self.scroll_y < -max_height:
            self.scroll_y = self.game.screen.get_height() + 50

        # Input handling
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.state_manager.change_state("MAIN_MENU")

    def draw(self, surface):
        surface.fill((10, 10, 15))

        # Draw title
        title = self.font_title.render("CREDITS", True, (255,255,255))
        surface.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 40))

        # Draw scrolling text
        y = int(self.scroll_y)
        for line in self.credits:
            text = self.font_normal.render(line, True, (220, 220, 220))
            x = self.screen.get_width() // 2 - text.get_width() // 2
            surface.blit(text, (x, y))
            y += 60

        # Draw cursor
        self.game.cursor.draw(surface)
