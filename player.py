import time

import CONST as c

class Player:
    PLAYER_COLOR = {1:c.RED, 2:c.BLUE}
    TIME_LIMIT = 5
    
    def __init__(self, board_size, left_sec=30):
        self.size = board_size
        self.is_game_over = False
        self.limit = c.SEC * 30
        self.score = 0
        self.cursor_pos = {'x':1, 'y':1} # y | x
        self.counting_start = 0

    def move(self, direction):
        x_move, y_move = direction[1], direction[0]
        if self.is_inside(self.cursor_pos['y']+y_move, self.cursor_pos['x']+x_move):
            self.cursor_pos['y'] += y_move
            self.cursor_pos['x'] += x_move

    def is_inside(self, y, x):
        return True if (0 <= y <= (self.size-3)) and (0 <= x <= (self.size-3)) else False

    def time_up(self):
        return Player.TIME_LIMIT < self.time_left()

    def time_left(self):
        return time.time() - self.counting_start