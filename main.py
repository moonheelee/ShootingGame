import pygame
import sys
import pygame.font
from player import Player
from bullet import Bullet
from enemy import Enemy
from target_bullet import TargetBullet
from explosion import Explosion

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Raiden-like Shooting Game')

pygame.font.init()
font = pygame.font.Font(None, 36)

# Sprite groups
player_group = pygame.sprite.Group()
player = Player(WIDTH, HEIGHT)
player_group.add(player)

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

clock = pygame.time.Clock()
enemy_spawn_time = pygame.time.get_ticks()
score = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.x + player.rect.width // 2 - 8, player.rect.y)
                bullet_group.add(bullet)
            elif event.key == pygame.K_s:
                target_enemy = None
                for enemy in enemy_group:
                    if not any(isinstance(bullet, TargetBullet) and bullet.target == enemy for bullet in bullet_group):
                        target_enemy = enemy
                        break
                if target_enemy:
                    bullet = TargetBullet(player.rect.x + player.rect.width // 2 - 8, player.rect.y, target_enemy)
                    bullet_group.add(bullet)

    # Spawn enemies
    if pygame.time.get_ticks() - enemy_spawn_time > 1000:
        enemy = Enemy(WIDTH, HEIGHT)
        enemy_group.add(enemy)
        enemy_spawn_time = pygame.time.get_ticks()

    # Detect collisions
    collided_enemies = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
    for enemy in collided_enemies:
        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
        explosion_group.add(explosion)
    score += len(collided_enemies)

    collided_player = pygame.sprite.spritecollide(player, enemy_group, True)
    if len(collided_player) > 0:
        # Player collided with enemy
        player.kill()
        explosion = Explosion(player.rect.centerx, player.rect.centery)
        explosion_group.add(explosion)
        for sprite in enemy_group.sprites():
            explosion = Explosion(sprite.rect.centerx, sprite.rect.centery)
            explosion_group.add(explosion)
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()

    screen.fill((0, 0, 0))
    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    explosion_group.draw(screen)
    player_group.update()
    bullet_group.update()
    enemy_group.update()
    explosion_group.update()

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)
