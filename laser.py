import pygame
from pygame import sprite


class Laser(sprite.Sprite):
    speed = 5
    height = 600

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((2, 4))
        self.image.fill("white")
        self.rect = self.image.get_rect(center=pos)

    def delete(self):
        if self.rect.y < -50 or self.rect.y > self.height + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.delete()

    def move_up(self):
        self.rect.y -= self.speed
        self.delete()
