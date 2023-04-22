import pygame
import math


class TargetBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 6
        self.target = target

    def update(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        self.rect.x += math.cos(math.radians(angle)) * self.speed
        self.rect.y += math.sin(math.radians(angle)) * self.speed
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.top > 600 or self.rect.bottom < 0:
            self.kill()
