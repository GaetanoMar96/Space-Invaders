import pygame, sys
from player import Player
import obstacles
from aliens import Alien
from laser import Laser
import random


class Game:
    def __init__(self):
        # Player set up
        player_sprite = Player(pos=(width / 2, height), speed=5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health setup
        self.lives = 3
        filename = "images/spaceship_new.png"
        bg_color = (246, 246, 246)
        self.image = pygame.image.load(filename)
        self.resize = (40, 20)
        self.live_surf = pygame.transform.scale(self.image, self.resize)
        self.live_surf.set_colorkey(bg_color)
        self.live_surf.convert_alpha()
        self.live_x_start = width - (self.live_surf.get_size()[0] * 2 + 20)

        # score setup
        self.score = 0
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        # Obstacle set up
        self.shape = obstacles.shape
        self.block_size = 6
        self.num_obs = 5
        self.blocks = pygame.sprite.Group()
        self.generator = [num * width / self.num_obs for num in range(self.num_obs)]
        self.create_multiple_obs(*self.generator, x_start=25, y_start=480)

        # Aliens set up
        self.aliens = pygame.sprite.Group()
        self.aliens_lasers = pygame.sprite.Group()
        self.num_aliens = 8
        self.direction = 1
        rows = ["red", "red", "white", "white", "green", "green"]
        self.create_aliens(offset_x=60, x_start=60, y_start=40, rows=rows, cols=self.num_aliens)

    def run(self):
        # Player check
        self.player.sprite.lasers.draw(screen)
        self.player.update()
        self.player.draw(screen)

        self.display_lives()
        self.display_score()
        # Aliens check
        self.aliens.update(self.direction)
        self.check_aliens()
        self.aliens_lasers.update()

        # Draw
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.aliens_lasers.draw(screen)

        # collisions
        self.check_collisions()

        # victory
        self.check_victory()

    def create_obstacle(self, offset_x, x_start, y_start):
        for row_idx, row in enumerate(self.shape):
            for col_idx, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_idx * self.block_size + offset_x
                    y = y_start + row_idx * self.block_size
                    block = obstacles.Block(self.block_size, x, y)
                    self.blocks.add(block)

    def create_multiple_obs(self, *offset_x, x_start, y_start):
        for offset in offset_x:
            self.create_obstacle(offset, x_start, y_start)

    def create_aliens(self, offset_x, x_start, y_start, rows, cols):

        for row_idx, row in enumerate(rows):
            color = rows[row_idx]
            for col_idx, col in enumerate(range(cols)):
                x = x_start * col_idx + offset_x
                y = y_start * row_idx
                alien = Alien(pos=(x, y), color=color)
                self.aliens.add(alien)

    def check_aliens(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= width:
                self.direction = -1
                self.aliens_move_down(1)
            elif alien.rect.left < 0:
                self.direction = 1
                self.aliens_move_down(1)

    def aliens_move_down(self, distance_y):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance_y

    def alien_shoot_laser(self):
        if self.aliens.sprites():
            random_alien = random.choice(self.aliens.sprites())
            laser_sprite = Laser(pos=random_alien.rect.center)
            self.aliens_lasers.add(laser_sprite)

    def check_collisions(self):
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Check obstacles collision
                if pygame.sprite.spritecollide(laser, self.blocks, dokill=True):
                    laser.kill()
                # Check aliens collision
                if self.aliens.sprites():
                    aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, dokill=True)
                    for alien in aliens_hit:
                        self.score += alien.value
                        laser.kill()

        if self.aliens_lasers:
            for laser in self.aliens_lasers:
                # Check obstacles collision
                if pygame.sprite.spritecollide(laser, self.blocks, dokill=True):
                    laser.kill()
                # Check player collision
                if pygame.sprite.spritecollide(laser, self.player, dokill=False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        # aliens
        if self.aliens.sprites():
            for alien in self.aliens.sprites():
                pygame.sprite.spritecollide(alien, self.blocks, dokill=True)

                if pygame.sprite.spritecollide(alien, self.player, dokill=True):
                    pygame.quit()
                    sys.exit()
        else: self.check_victory()

    def display_lives(self):

        for live in range(self.lives - 1):
            x = self.live_x_start + (live * self.live_surf.get_size()[0] + 10)
            screen.blit(self.live_surf, (x,8))

    def display_score(self):
        score_surf = self.font.render(f"Score: {self.score}", False, "white")
        score_rect = score_surf.get_rect(topleft=(0, 0))
        screen.blit(score_surf, score_rect)

    def check_victory(self):
        if not self.aliens.sprites():
            self.font = pygame.font.Font("freesansbold.ttf", 50)
            score_surf = self.font.render(f"You Won!", False, "white")
            score_rect = score_surf.get_rect(center=(300,300))
            screen.blit(score_surf, score_rect)


if __name__ == '__main__':
    pygame.init()
    width = 600
    height = 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == ALIENLASER:
                game.alien_shoot_laser()

        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        clock.tick(60)