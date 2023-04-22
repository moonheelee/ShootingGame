import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size=50):
        super().__init__()
        self.images = []
        self.index = 0
        self.rect = pygame.Rect(x - size / 2, y - size / 2, size, size)
        for i in range(9):
            image = pygame.Surface((size, size), pygame.SRCALPHA)
            alpha = (9 - i) * 28
            pygame.draw.circle(image, (255, 255, 255, alpha), (size // 2, size // 2), size // 2)
            self.images.append(image)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=self.rect.center)
        self.timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.timer > 40:
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]
                self.rect = self.image.get_rect(center=self.rect.center)
            self.timer = now
