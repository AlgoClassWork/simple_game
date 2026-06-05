#pip install pygame
import random
from pygame import *

WIN_W, WIN_H = 700, 500
PLAYER_SIZE = 100
ENEMY_SIZE = 80
PLAYER_SPEED = 5
BASE_ENEMY_SPEED = 1.5        # начальная скорость врага
SPAWN_INTERVAL = 5            # секунд между появлением нового врага
MAX_ENEMIES = 8

init()
window = display.set_mode((WIN_W, WIN_H))
display.set_caption("Chase Game")

background = image.load('background.png')
background = transform.scale(background, (WIN_W, WIN_H))

player_img = image.load('player.png')
player_img = transform.scale(player_img, (PLAYER_SIZE, PLAYER_SIZE))

enemy_img = image.load('enemy.png')
enemy_img = transform.scale(enemy_img, (ENEMY_SIZE, ENEMY_SIZE))

font_big   = font.SysFont(None, 72)
font_small = font.SysFont(None, 36)

clock = time.Clock()


def spawn_enemy():
    """Появление нового врага у случайного края экрана."""
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        return [random.randint(0, WIN_W - ENEMY_SIZE), -ENEMY_SIZE]
    elif side == 'bottom':
        return [random.randint(0, WIN_W - ENEMY_SIZE), WIN_H]
    elif side == 'left':
        return [-ENEMY_SIZE, random.randint(0, WIN_H - ENEMY_SIZE)]
    else:
        return [WIN_W, random.randint(0, WIN_H - ENEMY_SIZE)]


def reset_game():
    player_rect = Rect(WIN_W // 2 - PLAYER_SIZE // 2,
                       WIN_H // 2 - PLAYER_SIZE // 2,
                       PLAYER_SIZE, PLAYER_SIZE)
    enemies = [[175.0, 175.0]]   # стартовый враг
    return player_rect, enemies, time.get_ticks(), time.get_ticks()


def run_game():
    player_rect, enemies, start_ticks, last_spawn = reset_game()
    game_over = False
    survived_sec = 0

    while True:
        dt = clock.tick(60)

        # ---------- события ----------
        for some_event in event.get():
            if some_event.type == QUIT:
                quit()
            if game_over and some_event.type == KEYDOWN:
                if some_event.key == K_r:
                    player_rect, enemies, start_ticks, last_spawn = reset_game()
                    game_over = False
                elif some_event.key == K_ESCAPE:
                    quit()

        if game_over:
            # -------- экран Game Over --------
            window.blit(background, (0, 0))
            overlay = Surface((WIN_W, WIN_H), SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            window.blit(overlay, (0, 0))

            go_text  = font_big.render("GAME OVER", True, (220, 50, 50))
            sc_text  = font_small.render(f"Вы продержались: {survived_sec} сек", True, (255, 255, 255))
            r_text   = font_small.render("R — играть снова   ESC — выход", True, (200, 200, 200))

            window.blit(go_text,  go_text.get_rect(center=(WIN_W // 2, WIN_H // 2 - 60)))
            window.blit(sc_text,  sc_text.get_rect(center=(WIN_W // 2, WIN_H // 2 + 10)))
            window.blit(r_text,   r_text.get_rect(center=(WIN_W // 2, WIN_H // 2 + 60)))
            display.update()
            continue

        # ---------- движение игрока ----------
        keys = key.get_pressed()
        if keys[K_LEFT]  or keys[K_a]: player_rect.x -= PLAYER_SPEED
        if keys[K_RIGHT] or keys[K_d]: player_rect.x += PLAYER_SPEED
        if keys[K_UP]    or keys[K_w]: player_rect.y -= PLAYER_SPEED
        if keys[K_DOWN]  or keys[K_s]: player_rect.y += PLAYER_SPEED

        # границы экрана для игрока
        player_rect.clamp_ip(Rect(0, 0, WIN_W, WIN_H))

        # ---------- таймер и усложнение ----------
        now = time.get_ticks()
        survived_sec = (now - start_ticks) // 1000
        # скорость врагов растёт каждые 5 секунд
        enemy_speed = BASE_ENEMY_SPEED + survived_sec * 0.08

        # ---------- появление новых врагов ----------
        if now - last_spawn >= SPAWN_INTERVAL * 1000 and len(enemies) < MAX_ENEMIES:
            enemies.append(spawn_enemy())
            last_spawn = now

        # ---------- движение врагов ----------
        px, py = float(player_rect.x), float(player_rect.y)
        for e in enemies:
            dx = px - e[0]
            dy = py - e[1]
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist > 0:
                e[0] += enemy_speed * dx / dist
                e[1] += enemy_speed * dy / dist

        # ---------- столкновение ----------
        for e in enemies:
            enemy_rect = Rect(int(e[0]), int(e[1]), ENEMY_SIZE, ENEMY_SIZE)
            if player_rect.colliderect(enemy_rect):
                game_over = True
                break

        # ---------- отрисовка ----------
        window.blit(background, (0, 0))
        for e in enemies:
            window.blit(enemy_img, (int(e[0]), int(e[1])))
        window.blit(player_img, player_rect)

        # HUD
        timer_surf = font_small.render(f"Время: {survived_sec} сек", True, (255, 255, 255))
        count_surf = font_small.render(f"Врагов: {len(enemies)}", True, (255, 200, 50))
        window.blit(timer_surf, (10, 10))
        window.blit(count_surf, (10, 45))

        display.update()


run_game()