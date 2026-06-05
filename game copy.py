#pip install pygame
from pygame import *

window = display.set_mode((700, 500))

background = image.load('background.png')
background = transform.scale(background, (700, 500))

while True:
    for some_event in event.get():
        if some_event.type == QUIT:
            quit()

    window.blit(background, (0, 0))

    display.update()
        