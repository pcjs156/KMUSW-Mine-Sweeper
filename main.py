import pygame as pg
import time

import CONST

# Pygame Initializing
pg.init()
SIZE = WIDTH, HEIGHT = CONST.WIDTH, CONST.HEIGHT
pg.display.set_caption("지뢰찾기")
screen = pg.display.set_mode(SIZE)

# FPS / Clock
FPS = 60
clock = pg.time.Clock()

running = True
while running :
    dt = clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(CONST.BG_COLOR)

    pg.display.update()