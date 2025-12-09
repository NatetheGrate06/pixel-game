import pygame

class TextureManager:
    cache = {}

    @staticmethod
    def load(path, scale=None) :
        if path in TextureManager.cache:
            return TextureManager.cache[path]
        
        img = pygame.image.load(path).convert_alpha()

        if scale is not None :
            img = pygame.transform.scale(img, scale)

        TextureManager.cache[path] = img
        return img