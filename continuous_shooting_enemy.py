import pygame
import random
from enemy_bullet import EnemyBullet


class ContinuousShootingEnemy(pygame.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, args[0] - self.rect.width)
        self.rect.y = -self.rect.height
        self.height = args[1]
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_interval = random.randint(400, 1200)  # in milliseconds
        self.target = kwargs['target']
        self.bullet_group = kwargs['bullet_group']
        self.move = True

    def update(self):
        if self.move:
            self.rect.y += 5
            if self.rect.y > self.height:
                self.kill()

        if pygame.time.get_ticks() - self.last_shot_time > self.shot_interval:
            self.last_shot_time = pygame.time.get_ticks()
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.height, [self.target.rect.x, self.target.rect.y])
            self.bullet_group.add(bullet)
            self.shot_interval = 1000
            self.move = False
