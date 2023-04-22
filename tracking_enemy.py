import pygame
import random
from enemy_bullet import EnemyBullet


class TrackingEnemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, target, bullet_group):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((128, 255, 128))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_interval = random.randint(300, 800)  # in milliseconds
        self.target = target
        self.bullet_group = bullet_group
        self.has_shot = False

    def update(self):
        if not self.has_shot:
            self.rect.y += 5
            if self.rect.y > self.screen_height:
                self.kill()

        if pygame.time.get_ticks() - self.last_shot_time > self.shot_interval:
            self.last_shot_time = pygame.time.get_ticks()
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.screen_height, [self.target.rect.x, self.target.rect.y])
            self.bullet_group.add(bullet)
            self.shot_interval = 600
            self.has_shot = True

        if self.has_shot:
            # Move horizontally to track the player's position
            if self.rect.centerx < self.target.rect.centerx:
                self.rect.x += 1
            elif self.rect.centerx > self.target.rect.centerx:
                self.rect.x -= 1
