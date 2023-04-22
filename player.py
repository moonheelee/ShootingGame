import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = args[0] // 2
        self.rect.y = args[1] - 80
        self.width = args[0]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Keep the player within the screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > self.width - self.rect.width:
            self.rect.x = self.width - self.rect.width
