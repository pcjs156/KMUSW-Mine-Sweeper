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

# Audio
pg.mixer.music.load('./resource/sounds/bgm/default_music.wav')
boom_sound = pg.mixer.Sound('./resource/sounds/effects/boom.wav')

running = True
gameover = False
defeat_by_mine = False
defeat_by_time = False
alarm_txt = ""
while running :
    # Game Setting
    MINE = 10
    GAMEBOARD_SIZE = c.INNER
    board = Board(GAMEBOARD_SIZE, MINE)
    board_size = board.size

    # BGM
    pg.mixer.music.play(-1)

    # About Rendering
    board_start_pos = (c.CELL_SIZE, 4*c.CELL_SIZE)
    board.p[board.now].counting_start = time.time()
    while not gameover :
        if board.p[board.now].time_up():
            defeat_by_time = True
            break

        dt = clock.tick(FPS)

        player_txt = "PLAYER {}'s TURN".format(board.now)
        guide_txt = "Press SPACE to Open Block"
        
        p1_score = "P1 SCORE : {}".format(board.p[1].score)
        p2_score = "P2 SCORE : {}".format(board.p[2].score)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE :
                    code = board.choose(board.p[board.now].cursor_pos['y']+1, board.p[board.now].cursor_pos['x']+1)
                    if code is c.ERROR :
                        alarm_txt = "Already Opened"
                    elif code is c.BOOM:
                        gameover = True # gameover는 게임 종료
                        defeat_by_mine = True # defeat_by_mine은 지뢰를 밟아서 누군가 진 경우
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
        Rendering.render_text(screen, alarm_txt, 10, (140, c.CELL_SIZE*2-40), c.BLACK)
        Rendering.render_text(screen, player_txt, c.FONT_SIZE, (93, c.CELL_SIZE*2-20), Player.PLAYER_COLOR[board.now])
        Rendering.render_text(screen, guide_txt, 10, (112, c.CELL_SIZE*2), c.BLACK)
        Rendering.render_text(screen, p1_score, 12, (0, 0), c.RED)
        Rendering.render_text(screen, p2_score, 12, (c.WIDTH-80, 0), c.BLUE)

        # 남은 시간
        sec_txt = '{:0.1f}'.format(board.p[board.now].time_left())
        sec_color = c.BLACK if board.p[board.now].time_left() < Player.TIME_LIMIT//3*2 else c.RED
        Rendering.render_text(screen, sec_txt, 20, (170, c.CELL_SIZE*2+20), sec_color)
        
        pg.display.update()

        if board.left_block == board.mine_cnt :
            gameover = True
    

    # 시간초과
    if defeat_by_time:
        result_message = 'TIME UP!'
        print("Player {}님의 시간이 모두 종료되었습니다.".format(board.now))
        winner = 1 if board.now == 2 else 2
    # 지뢰밟음
    elif defeat_by_mine:
        result_message = 'BOOOOM!'
        print("Player {}님이 지뢰를 선택하셨습니다.".format(board.now))
        winner = 1 if board.now == 2 else 2
    # 남은 지뢰가 없음
    else:
        result_message = 'PERFECT!'
        print("Player {}님의 점수가 더 낮습니다.".format(board.now))
        p1_score = board.p[1].score
        p2_score = board.p[2].score
        winner = 1 if p1_score > p2_score else 2

    print("WINNER: Player {}".format(winner))


    pg.mixer.music.stop()
    pg.mixer.Sound.play(boom_sound)
    restart = False
    keydown = False
    while True:
        screen.fill(c.BG_COLOR)
        Rendering.render_text(screen, result_message, 40, (90, c.CELL_SIZE*2+40), c.BLACK)
        winner_color = c.RED if winner == 1 else c.BLUE
        Rendering.render_text(screen, 'WINNER: Player {}'.format(winner), 30, (50, c.CELL_SIZE*2+80), winner_color)
        Rendering.render_text(screen, 'Press Spacebar to play again', 15, (75, c.CELL_SIZE*2+110), c.BLACK)
        Rendering.render_text(screen, 'Or Press X Key to stop playing', 15, (70, c.CELL_SIZE*2+125), c.BLACK)
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE :
                    restart = True
                    keydown = True
                    break
                if event.key == pg.K_x :
                    restart = False
                    keydown = True
                    break
        if keydown:
            break
    
    if restart :
        gameover = False
        continue
    else:
        break