import pygame as pg
import time

import CONST as c
from gameboard import Board
from rendering import Rendering
from player import Player

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

    player_txt = "PLAYER {}'s TURN".format(board.now)
    guide_txt = "Press SPACE to shift player"
    open_txt = "Press X to open Block"

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE :
                board.change_player()
            elif event.key == pg.K_LEFT:
                board.p[board.now].move(c.V_DICT["LEFT"])
            elif event.key == pg.K_RIGHT:
                board.p[board.now].move(c.V_DICT["RIGHT"])
            elif event.key == pg.K_UP:
                board.p[board.now].move(c.V_DICT["UP"])
            elif event.key == pg.K_DOWN:
                board.p[board.now].move(c.V_DICT["DOWN"])
            elif event.key == pg.K_x:
                # X를 누르면 칸을 연다
                pass
            
    # 배경 칠하기    
    screen.fill(c.BG_COLOR)

    # 게임판 그리기
    pg.draw.rect(screen, c.BOARD_COLOR, (c.CELL_SIZE, 4*c.CELL_SIZE, c.INNER*c.CELL_SIZE, c.INNER*c.CELL_SIZE))
    for i in range(1, board_size-1):
        for j in range(1, board_size-1):
            Rendering.render(screen, c.CELL_SIZE, board_start_pos, i-1, j-1, board.board[i][j])

    player_now = board.p[board.now]
    Rendering.render_cursor(screen, c.CELL_SIZE, board_start_pos, player_now.cursor_pos['y'], player_now.cursor_pos['x'], board.now)

    # 누가 플레이중?
    Rendering.render_text(screen, player_txt, c.FONT_SIZE, (93, c.CELL_SIZE*2-20), Player.PLAYER_COLOR[board.now])
    Rendering.render_text(screen, guide_txt, 10, (112, c.CELL_SIZE*2), c.BLACK)
    Rendering.render_text(screen, open_txt, 10, (127, c.CELL_SIZE*2+10), c.BLACK)

    pg.display.update()