import pygame
from pygame import sprite


class Alien(sprite.Sprite):
    width = 600
    height = 600
    bg_color = (247, 247, 247)

    def __init__(self, pos, color):
        super().__init__()
        self.filename = "images/alien_" + color + ".png"

        if color == "red": self.value = 300
        if color == "white": self.value = 200
        else: self.value = 100

        self.image = pygame.image.load(self.filename)
        self.resize = (50, 30)
        self.image = pygame.transform.scale(self.image, self.resize)
        self.image.set_colorkey(self.bg_color)
        self.image.convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, direction):
        self.rect.x += direction



