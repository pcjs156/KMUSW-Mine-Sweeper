import pygame as pg
import time

import CONST as c
from gameboard import Board
from rendering import Rendering

# Pygame Initializing
pg.init()
pg.display.set_caption("지뢰찾기")
screen = pg.display.set_mode(c.SIZE)

# FPS / Clock
FPS = 60
clock = pg.time.Clock()

# Game Setting
MINE = 3
GAMEBOARD_SIZE = c.INNER
board = Board(GAMEBOARD_SIZE, 3)
board_size = board.size

# About Rendering
board_start_pos = (c.CELL_SIZE, 4*c.CELL_SIZE)

running = True
while running :
    dt = clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.fill(c.BG_COLOR)
    # 게임판 그리기
    pg.draw.rect(screen, c.BOARD_COLOR, (c.CELL_SIZE, 4*c.CELL_SIZE, c.INNER*c.CELL_SIZE, c.INNER*c.CELL_SIZE))
    for i in range(1, board_size-1):
        for j in range(1, board_size-1):
            Rendering.render(screen, c.CELL_SIZE, board_start_pos, i-1, j-1, board.board[i][j])

    pg.display.update()