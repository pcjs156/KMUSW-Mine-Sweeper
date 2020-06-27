import pygame as pg
import time
import sys

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

# Audio
pg.mixer.music.load('./bgm/default_music.wav')
pg.mixer.music.play(-1)

running = True
gameover = False
defeat = False
alarm_txt = ""
while running :
    board.p[board.now].counting_start = time.time()
    while not gameover :
        if board.p[board.now].time_up():
            print("Player {}님의 시간이 모두 종료되었습니다.".format(board.now))
            break

        dt = clock.tick(FPS)

        player_txt = "PLAYER {}'s TURN".format(board.now)
        guide_txt = "Press SPACE to Open Block"
        
        p1_score = "P1 SCORE : {}".format(board.p[1].score)
        p2_score = "P2 SCORE : {}".format(board.p[2].score)

        for event in pg.event.get():
            print(board.p[board.now].cursor_pos['x'], board.p[board.now].cursor_pos['y'])
            if event.type == pg.QUIT:
                sys.exit()

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
                        board.p[board.now].counting_start = time.time()

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
        Rendering.render_text(screen, p1_score, 12, (0, 0), c.RED)
        Rendering.render_text(screen, p2_score, 12, (c.WIDTH-80, 0), c.BLUE)

        # 남은 시간
        sec_txt = '{:0.1f}'.format(board.p[board.now].time_left())
        Rendering.render_text(screen, sec_txt, 20, (170, c.CELL_SIZE*2+20), c.BLACK)
        
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