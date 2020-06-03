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
MINE = 10
GAMEBOARD_SIZE = c.INNER
board = Board(GAMEBOARD_SIZE, MINE)
board_size = board.size

# About Rendering
board_start_pos = (c.CELL_SIZE, 4*c.CELL_SIZE)

running = True
gameover = False
defeat = False
while running :
    while not gameover :
        dt = clock.tick(FPS)

        player_txt = "PLAYER {}'s TURN".format(board.now)
        guide_txt = "Press SPACE to Open Block"
        alarm_txt = ""

        for event in pg.event.get():
            print(board.p[board.now].cursor_pos['x'], board.p[board.now].cursor_pos['y'])
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE :
                    code = board.choose(board.p[board.now].cursor_pos['y']+1, board.p[board.now].cursor_pos['x']+1)
                    if code is c.ERROR :
                        alarm_txt = "Already Opened"
                    elif code is c.BOOM:
                        gameover = True # gameover는 게임 종료
                        defeat = True # defeat은 지뢰를 밟아서 누군가 진 경우
                    else :
                        alarm_txt = ""
                        board.change_player()

                elif event.key == pg.K_LEFT:
                    board.p[board.now].move(c.V_DICT["LEFT"])
                elif event.key == pg.K_RIGHT:
                    board.p[board.now].move(c.V_DICT["RIGHT"])
                elif event.key == pg.K_UP:
                    board.p[board.now].move(c.V_DICT["UP"])
                elif event.key == pg.K_DOWN:
                    board.p[board.now].move(c.V_DICT["DOWN"])
                
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
        Rendering.render_text(screen, alarm_txt, 10, (127, c.CELL_SIZE*2-40), c.BLACK)
        Rendering.render_text(screen, player_txt, c.FONT_SIZE, (93, c.CELL_SIZE*2-20), Player.PLAYER_COLOR[board.now])
        Rendering.render_text(screen, guide_txt, 10, (112, c.CELL_SIZE*2), c.BLACK)
        pg.display.update()

        
        if board.left_block == board.mine_cnt :
            gameover = True
    
    if defeat:
        print("PLAYER {} is defeated".format(board.now))
    else:
        p1_score = board.p[1].score
        p2_score = board.p[2].score
        winner = 1 if p1_score > p2_score else 2
        print("WINNER : {}".format(winner))
    break