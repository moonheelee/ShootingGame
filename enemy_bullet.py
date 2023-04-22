import pygame
import math


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, height, player_pos):
        super().__init__()
        self.image = pygame.Surface((8, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.height = height
        self.speed = 5
        self.player_pos = player_pos

    def update(self):
        dx = self.player_pos[0] - self.rect.centerx
        dy = (self.height + self.rect.height) - self.rect.centery
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist != 0:
            dx_norm = dx / dist
            dy_norm = dy / dist
            self.rect.x += dx_norm * self.speed
            self.rect.y += dy_norm * self.speed
        if self.rect.bottom < 0:
            self.kill()
