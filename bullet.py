import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target=None):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -10
        self.target = target

    def update(self):
        self.rect.y -= 10
        if self.rect.y < -self.rect.height:
            self.kill()
