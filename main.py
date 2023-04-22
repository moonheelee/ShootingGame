import pygame
import sys
from player import Player
from bullet import Bullet
from enemy import Enemy
from shooting_enemy import ShootingEnemy
from continuous_shooting_enemy import ContinuousShootingEnemy
from target_bullet import TargetBullet
from explosion import Explosion
from tracking_enemy import TrackingEnemy

# Constants
WIDTH, HEIGHT = 800, 600
FRAME_RATE = 60
SPECIAL_BULLET_MAX = 5
SPECIAL_BULLET_RECHARGE_TIME = 10000
ENEMY_SPAWN_INTERVAL = 1000

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Raiden-like Shooting Game')

pygame.font.init()
score_font = pygame.font.Font(None, 36)
special_bullet_font = pygame.font.Font(None, 28)

# Sprite groups
player_group = pygame.sprite.Group()
player = Player(WIDTH, HEIGHT)
player_group.add(player)

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

clock = pygame.time.Clock()
enemy_spawn_time = pygame.time.get_ticks()
score = 0
enemy_count = 0

# Special bullet variables
special_bullet_count = SPECIAL_BULLET_MAX
special_bullet_timer = 0


def handle_input():
    global special_bullet_count
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.x + player.rect.width // 2 - 8, player.rect.y)
                bullet_group.add(bullet)
            elif event.key == pygame.K_s:
                if special_bullet_count > 0:
                    target_enemy = find_target_enemy()
                    if target_enemy:
                        bullet = TargetBullet(player.rect.x + player.rect.width // 2 - 8, player.rect.y, target_enemy)
                        bullet_group.add(bullet)
                        special_bullet_count -= 1


def find_target_enemy():
    for enemy in enemy_group:
        if not any(isinstance(bullet, TargetBullet) and bullet.target == enemy for bullet in bullet_group):
            return enemy
    return None


def recharge_special_bullet():
    global special_bullet_count
    global special_bullet_timer
    if pygame.time.get_ticks() - special_bullet_timer > SPECIAL_BULLET_RECHARGE_TIME:
        special_bullet_count = SPECIAL_BULLET_MAX
        special_bullet_timer = pygame.time.get_ticks()


def spawn_enemies():
    global enemy_count
    global enemy_spawn_time
    if pygame.time.get_ticks() - enemy_spawn_time > ENEMY_SPAWN_INTERVAL:
        enemy_count += 1
        enemy = None
        if enemy_count % 3 == 0:
            enemy = ShootingEnemy(WIDTH, HEIGHT, target=player, bullet_group=enemy_bullet_group)
        if enemy_count % 5 == 0:
            enemy = ContinuousShootingEnemy(WIDTH, HEIGHT, target=player, bullet_group=enemy_bullet_group)
        if enemy_count % 7 == 0:
            enemy = TrackingEnemy(WIDTH, HEIGHT, target=player, bullet_group=enemy_bullet_group)
        if enemy is None:
            enemy = Enemy(WIDTH, HEIGHT)
        enemy_group.add(enemy)
        enemy_spawn_time = pygame.time.get_ticks()


def handle_collisions():
    global score
    global collided_player
    global destroyed_player

    collided_enemies = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
    for enemy in collided_enemies:
        explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
        explosion_group.add(explosion)
    score += len(collided_enemies)

    collided_player = pygame.sprite.spritecollide(player, enemy_group, True)
    destroyed_player = pygame.sprite.spritecollide(player, enemy_bullet_group, True)
    if len(collided_player) > 0 or len(destroyed_player) > 0:
        return False
    return True


def end_game():
    for sprite in enemy_group.sprites():
        explosion = Explosion(sprite.rect.centerx, sprite.rect.centery)
        explosion_group.add(explosion)

    game_over_text = score_font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text,
                (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

    restart_text = score_font.render("Press R to restart or Q to quit", True, (255, 255, 255))
    screen.blit(restart_text,
                (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False
            if event.type == pygame.QUIT:
                return False


def update_sprites():
    player_group.update()
    bullet_group.update()
    enemy_group.update()
    enemy_bullet_group.update()
    explosion_group.update()


def render():
    screen.fill((0, 0, 0))
    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    enemy_bullet_group.draw(screen)
    explosion_group.draw(screen)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    special_bullet_text = special_bullet_font.render(f"Special Bullets: {special_bullet_count}", True, (255, 255, 255))
    special_bullet_rect = special_bullet_text.get_rect()
    special_bullet_rect.topleft = (10, 40)
    screen.blit(special_bullet_text, special_bullet_rect)

    pygame.display.flip()
    clock.tick(FRAME_RATE)


# Main game loop
def reset_game():
    global player

    # Clear all sprite groups
    player_group.empty()
    bullet_group.empty()
    enemy_group.empty()
    enemy_bullet_group.empty()
    explosion_group.empty()

    # Add player back to the player_group
    player = Player(WIDTH, HEIGHT)
    player_group.add(player)


def main():
    global enemy_spawn_time
    global score
    global enemy_count
    global special_bullet_count
    global special_bullet_timer

    reset_game()

    enemy_spawn_time = pygame.time.get_ticks()
    score = 0
    enemy_count = 0
    special_bullet_count = SPECIAL_BULLET_MAX
    special_bullet_timer = 0

    # Main game loop
    while True:
        handle_input()
        recharge_special_bullet()
        spawn_enemies()
        is_game_running = handle_collisions()
        if not is_game_running:
            break
        update_sprites()
        render()

    return end_game()


# Run the main function
while True:
    main_result = main()
    if not main_result:
        pygame.quit()
        sys.exit()
