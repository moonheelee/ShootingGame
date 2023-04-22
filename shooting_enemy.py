import pygame
import random
from enemy_bullet import EnemyBullet


class ShootingEnemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, target, bullet_group):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.screen_height = screen_height
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_interval = random.randint(500, 900)  # in milliseconds
        self.target = target
        self.bullet_group = bullet_group
        self.fired = False

    def update(self):
        self.rect.y += 5
        if self.rect.y > self.screen_height:
            self.kill()

        if not self.fired and pygame.time.get_ticks() - self.last_shot_time > self.shot_interval:
            self.last_shot_time = pygame.time.get_ticks()
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.screen_height, [self.target.rect.x, self.target.rect.y])
            self.bullet_group.add(bullet)
            self.fired = True
