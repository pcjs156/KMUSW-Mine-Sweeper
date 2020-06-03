import pygame as pg

import CONST as c

class Rendering:
    cursor_list = (pg.image.load('img/p1_cursor.png'), pg.image.load('img/p2_cursor.png'))

    mine = pg.image.load('img/mine.png')
    icon_closed = pg.image.load('img/closed.png')

    num_icon = [
        pg.image.load('img/opened.png'),
        pg.image.load('img/icon_1.png'),
        pg.image.load('img/icon_2.png'),
        pg.image.load('img/icon_3.png'),
        pg.image.load('img/icon_4.png'),
        pg.image.load('img/icon_5.png'),
        pg.image.load('img/icon_6.png'),
        pg.image.load('img/icon_7.png'),
        pg.image.load('img/icon_8.png')
    ]

    @staticmethod
    def render(screen, cellsize, board_start_pos, y, x, element):
        screen.blit(Rendering.return_design(element, cellsize), (board_start_pos[0] + x*cellsize, board_start_pos[1] + y*cellsize))
    
    @staticmethod
    def render_cursor(screen, cellsize, board_start_pos, y, x, player_number):
        cursor = pg.transform.scale(Rendering.cursor_list[player_number-1], (cellsize, cellsize))
        screen.blit(cursor, (board_start_pos[0] + x*cellsize, board_start_pos[1] + y*cellsize))

    @staticmethod
    def return_design(element, cellsize):
        # element가 닫힌 칸인 경우
        if not element.is_opened :
            icon = Rendering.icon_closed
        else :
            # element가 Nothing인 경우
            icon = Rendering.num_icon[element.cnt]
    
        return pg.transform.scale(icon, (cellsize, cellsize))
    
    @staticmethod
    def render_text(screen, txt, size, pos, color):
        font = pg.font.Font('freesansbold.ttf', size)
        r = font.render(txt, True, color)
        screen.blit(r, pos)
