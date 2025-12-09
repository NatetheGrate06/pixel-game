# Audio/sound_manager.py
import pygame

# Global sound references
shoot = None
slash = None
player_die = None
grunt_die = None
brute_die = None
item_pickup = None

def load_sounds():
    global shoot, slash, player_die, grunt_die, brute_die, item_pickup

    # If already loaded, don't reload
    if shoot is not None:
        return

    shoot = pygame.mixer.Sound("Assets/SFX/gun-sound.mp3")
    slash = pygame.mixer.Sound("Assets/SFX/knife-sound.mp3")
    player_die = pygame.mixer.Sound("Assets/SFX/player-death.mp3")
    grunt_die = pygame.mixer.Sound("Assets/SFX/grunt-death.mp3")
    brute_die = pygame.mixer.Sound("Assets/SFX/brute-death.mp3")
    item_pickup = pygame.mixer.Sound("Assets/SFX/item-pickup.mp3")

    # tweak volumes if you want
    shoot.set_volume(0.2)
    slash.set_volume(0.5)
    player_die.set_volume(0.8)
    grunt_die.set_volume(0.7)
    brute_die.set_volume(0.7)
    item_pickup.set_volume(0.9)
