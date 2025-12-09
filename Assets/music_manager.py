import pygame

class MusicManager:
    def __init__(self):
        self.current = None

        self.tracks = {
            "menu" : "Assets/Music/menu-music.mp3",
            "level": "Assets/Music/level-music.mp3",
        }

        # Default volume
        self.volume = 0.5
        pygame.mixer.music.set_volume(self.volume)

    def play(self, name, fade_ms=800):
        """Play a track by name, with optional fade transition."""
        if name == self.current:
            return  # already playing

        if name not in self.tracks:
            print(f"[MusicManager] Track '{name}' not found.")
            return
        
        track_path = self.tracks[name]

        # Fade out old track
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)

        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play(-1, fade_ms=fade_ms)
        pygame.mixer.music.set_volume(self.volume)

        self.current = name

    def stop(self, fade_ms=600):
        pygame.mixer.music.fadeout(fade_ms)
        self.current = None

    def set_volume(self, volume):
        """0.0 to 1.0"""
        self.volume = volume
        pygame.mixer.music.set_volume(volume)
