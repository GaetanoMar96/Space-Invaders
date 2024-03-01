import pygame
from pygame import sprite


class Block(sprite.Sprite):
    color = "red"

    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x, y))


shape = [
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx'
]


