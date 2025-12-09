import pygame

class SettingsMenu:
    def __init__(self, screen, state_manager, game):
        self.screen = screen
        self.state_manager = state_manager
        self.game = game

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)

        self.volume = 1.0
        self.music_on = True

        self.resolutions = [
            (1600, 900),
            (1280, 720),
            (1024, 576),
            (800, 450),
        ]

        self.selected_resolution_index = 0

    def scale(self, value) :
        return int(value * self.game.resolution.uniform_scale)

    def update(self, events):
        for event in events:

            if event.type == pygame.KEYDOWN:

                # Go to previous resolution
                if event.key == pygame.K_a:
                    self.selected_resolution_index -= 1
                    if self.selected_resolution_index < 0:
                        self.selected_resolution_index = len(self.resolutions) - 1
                    self.apply_selected_resolution()

                # Go to next resolution
                elif event.key == pygame.K_d:
                    self.selected_resolution_index += 1
                    if self.selected_resolution_index >= len(self.resolutions):
                        self.selected_resolution_index = 0
                    self.apply_selected_resolution()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state_manager.change_state("MAIN_MENU")

                # Toggle music
                if event.key == pygame.K_m:
                    if not self.music_on :
                        self.music_on = True
                    else:
                        self.music_on = False

                    if self.music_on:
                        # turn music back on (resume whichever was last playing)
                        self.game.music.set_volume(self.volume)
                    else:
                        # mute music completely
                        self.game.music.set_volume(0.0)

                # Volume Control
                if event.key == pygame.K_UP:
                    self.volume = min(1.0, self.volume + 0.1)
                if event.key == pygame.K_DOWN:
                    self.volume = max(0.0, self.volume - 0.1)

            # Handle mouse clicks for resolution switching
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check which resolution the user clicked
                start_y = 300
                for i, (w, h) in enumerate(self.resolutions):
                    rect = pygame.Rect(600, start_y + i * 40, 400, 35)
                    if rect.collidepoint(mouse_x, mouse_y):
                        self.selected_resolution_index = i
                        self.apply_resolution(i)

    # For the keybinds
    def apply_selected_resolution(self):
        w, h = self.resolutions[self.selected_resolution_index]

        # Apply resolution to the game window
        self.game.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

        # Update scaling
        self.game.resolution.apply_resolution(w, h)

        print(f"[SETTINGS] Resolution changed to {w} x {h}")

    def apply_resolution(self, index):
        w, h = self.resolutions[index]

        # Change game window size
        self.game.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)

        # Apply scaling
        self.game.resolution.apply_resolution(w, h)

        print(f"Resolution changed to: {w}x{h}")

    def draw(self):
        self.screen.fill((10, 10, 14))

        scale = self.game.resolution.uniform_scale

        title = self.font.render("SETTINGS", True, (255, 255, 255))
        self.screen.blit(title, (self.scale(600), self.scale(80)))

        # Music toggle
        music_text = self.small_font.render(
            f"Music: {'ON' if self.music_on else 'OFF'} (Press M)",
            True, (220, 220, 220)
        )
        self.screen.blit(music_text, (self.scale(600), self.scale(200)))

        # Volume
        volume_text = self.small_font.render(
            f"Volume: {int(self.volume * 100)}% (UP/DOWN)",
            True, (220, 220, 220)
        )
        self.screen.blit(volume_text, (self.scale(600), self.scale(240)))

        # Resolution header
        res_title = self.small_font.render("Resolution:", True, (255, 255, 0))
        self.screen.blit(res_title, (self.scale(600), self.scale(280)))

        # Resolution list
        start_y = 300
        for i, (w, h) in enumerate(self.resolutions):
            label = f"{w} x {h}"
            color = (0, 200, 255) if i == self.selected_resolution_index else (180, 180, 180)

            text = self.small_font.render(label, True, color)
            self.screen.blit(text, (self.scale(600), self.scale(start_y + i * 40)))
