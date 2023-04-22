import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, args[0] - self.rect.width)
        self.rect.y = -self.rect.height
        self.height = args[1]

    def update(self):
        self.rect.y += 5
        if self.rect.y > self.height:
            self.kill()
