import CONST as c

class Player:
    def __init__(self, board_size):
        self.board_size = board_size
        self.is_game_over = False
        self.limit = c.SEC
        self.try_cnt = 0

    def is_inside(self, y, x):
        return True if (1 <= y <= (self.size-2)) and (1 <= x <= (self.size-2)) else False