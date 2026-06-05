from pygame import *

window = display.set_mode((700, 500))

background = image.load('background.png')
background = transform.scale(background, (700, 500))

player = image.load('player.png')
player = transform.scale(player, (100, 100))
player_x = 300
player_y = 400

enemy = image.load('enemy.png')
enemy = transform.scale(enemy, (100, 100))
enemy_x = 0
enemy_y = 0

clock = time.Clock()

while True:
    for some_event in event.get():
        if some_event.type == QUIT:
            quit()


    window.blit(background, (0, 0))
    window.blit(player, (player_x, player_y))
    window.blit(enemy, (enemy_x, enemy_y))

    keys = key.get_pressed()
    if keys[K_w]:
        player_y -= 5
    if keys[K_s]:
        player_y += 5
    if keys[K_a]:
        player_x -= 5
    if keys[K_d]:
        player_x += 5

    if enemy_x < player_x:
        enemy_x += 2
    if enemy_x > player_x:
        enemy_x -= 2
    if enemy_y < player_y:
        enemy_y += 2
    if enemy_y > player_y:
        enemy_y -= 2

    if abs(player_x - enemy_x) < 90 and abs(player_y - enemy_y) < 90:
        print("Game Over!")
        quit()
    
    display.update()
    clock.tick(60)
        
