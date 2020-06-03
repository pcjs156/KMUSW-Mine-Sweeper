import CONST as c

class Player:
    PLAYER_COLOR = {1:c.RED, 2:c.BLUE}
    
    def __init__(self, board_size):
        self.size = board_size
        self.is_game_over = False
        self.limit = c.SEC * 30
        self.try_cnt = 0
        self.cursor_pos = {'x':1, 'y':1} # y | x

    def move(self, direction):
        x_move, y_move = direction[1], direction[0]
        if self.is_inside(self.cursor_pos['y']+y_move, self.cursor_pos['x']+x_move):
            self.cursor_pos['y'] += y_move
            self.cursor_pos['x'] += x_move

    def is_inside(self, y, x):
        return True if (0 <= y <= (self.size-3)) and (0 <= x <= (self.size-3)) else False