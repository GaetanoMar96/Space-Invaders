import pygame
from pygame import sprite
from laser import Laser


class Player(sprite.Sprite):
    filename = "images/spaceship_new.png"
    width = 600
    height = 600
    bg_color = (246, 246, 246)

    def __init__(self, pos, speed):
        super().__init__()
        self.image = pygame.image.load(self.filename)
        self.image.set_colorkey(self.bg_color)
        self.image.convert_alpha()
        self.resize = (60, 30)
        self.image = pygame.transform.scale(self.image, self.resize)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x = (0, self.width - self.resize[0])
        self.laser_time = 0
        self.cool_down = 600
        self.ready = True
        self.lasers = pygame.sprite.Group()

    def get_key(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > min(self.max_x):
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < max(self.max_x):
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < self.height - self.resize[1]:
            self.rect.y += self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def shoot(self):
        self.lasers.add(Laser(pos=self.rect.center))

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.cool_down:
                self.ready = True

    def update(self):
        self.get_key()
        self.recharge()
        for laser in self.lasers.sprites():
            laser.move_up()
