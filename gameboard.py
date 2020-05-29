import pygame as pygame
from random import randint

import CONST
from elements import *

class Board:
    def __init__(self, size, mine):
        # 양 모서리와 변은 Wall로 지정할 것이므로
        self.size = size + 2
        self.mine_cnt = mine
        self.left_block = size * size

        # board : 실제 데이터를 담는 보드

        # 일단 전부 빈 칸으로 설정
        self.board = [[Nothing(i, j) for j in range(self.size)] for i in range(self.size)]
        # 벽면 만들기
        self.board[0] = [Wall(0, j) for j in range(self.size)]
        self.board[-1] = [Wall(0, j) for j in range(self.size)]
        for i in range(self.size):
            self.board[i][0] = Wall(i, 0)
            self.board[i][-1] = Wall(i, self.size-1)

        # {mine}개의 지뢰 설치
        for _ in range(mine):
            while True:
                i, j = randint(1, self.size-2), randint(1, self.size-2)
                if not isinstance(self.board[i][j], Mine) :
                    # 지뢰 주변 8칸에 1씩 올려서 표시
                    self.board[i][j] = Mine(i, j)
                    self.count_mine(i, j)
                    break

    # board[y][x] 자신+주변 9칸의 빈칸에 표시
    def count_mine(self, y, x):
        for v in CONST.VECTOR:
            if isinstance(self.board[y+v[0]][x+v[1]], Nothing):
                self.board[y+v[0]][x+v[1]].plus()


    # debug:True이면 실제 지뢰 정보가 담긴 보드 출력
    def print_board(self, debug=False):
        if debug:
            # 가로 가이드라인
            print('%3s' % ' ', end ='| ')
            for i in range(1, self.size-1):
                print('%3s' % i, end=' ')
            print()
            
            # 구분선
            print('-' * (4*self.size))

            # 세로 가이드라인 + 내용
            for i in range(1, self.size-1):
                print("%3s|" % i, end=' ')
                for j in range(1, self.size-1):
                    print('%3s' % self.board[i][j].icon(), end=' ')
                print()
            print()

        else :
            # 가로 가이드라인
            print('%3s' % ' ', end ='| ')
            for i in range(1, self.size-1):
                print('%3s' % i, end=' ')
            print()
            
            # 구분선
            print('-' * (4*self.size))

            # 세로 가이드라인 + 내용
            for i in range(1, self.size-1):
                print("%3s|" % i, end=' ')
                for j in range(1, self.size-1):
                    print('%3s' % self.board[i][j].icon() if self.board[i][j].is_opened else '%3s' % '#', end=' ')
                print()
            print()


    def print_bool_board(self):
        # 가로 가이드라인
        print('%3s' % ' ', end ='| ')
        for i in range(1, self.size-1):
            print('%3s' % i, end=' ')
        print()
        
        # 구분선
        print('-' * (4*self.size))

        # 세로 가이드라인 + 내용
        for i in range(1, self.size-1):
            print("%3s|" % i, end=' ')
            for j in range(1, self.size-1):
                print(self.board[i][j].is_opened, end=' ')
            print()
        print()


    # 보드 안의 좌표를 골랐는지 체크(아마 GUI로 옮기면서 할거같기는 한,,데 모르겠다)
    def is_inside(self, y, x):
        return True if (1 <= y <= (self.size-2)) and (1 <= x <= (self.size-2)) else False


    # 보드의 특정 좌표를 선택하여 상태코드 리턴
    def choose(self, y, x):
        # 보드를 벗어난 경우
        if not self.is_inside(y, x):
            print("1 ~ {} 사이의 값을 입력하세요.".format(self.size-2))
            return CONST.ERROR

        # 이미 공개된 칸인 경우
        elif self.board[y][x].is_opened is True :
            print("이미 공개된 칸입니다.")
            return CONST.ERROR

        # 비공개된 칸인 경우
        else :
            # 지뢰인 경우
            if isinstance(self.board[y][x], Mine) :
                print("지뢰를 선택하셨습니다!")
                return CONST.BOOM
            
            # 지뢰가 아닌 경우
            else :
                print("휴 살았당!")
                # self.start_chaining(y, x)
                self.open(y, x)
    

    '''
    으 재귀적으로 칸 여는거 넘 어렵다,, 일단 한칸씩 구현
    '''
    # # open_chaining 시작
    # def start_chaining(self, y, x):
    #     global chk
    #     chk = [[False for _ in range(self.size)] for _ in range(self.size)]
    #     # self.open_chaining(y, x, chk)
    #     self.open_chaining(y, x)


    # # 연쇄적으로 공개하기 : 벽이거나 지뢰를 만났을 경우 재귀 중단
    # def open_chaining(self, y, x):
    #     if chk[y][x] is True or isinstance(self.board[y][x], Wall) or isinstance(self.board[y][x], Mine) or self.board[y][x].cnt != 0:
    #         return
    #     else :
    #         for v in CONST.VECTOR:
    #             self.board[y][x].open()
    #             chk[y][x] = True
    #             self.open_chaining(y, x)
                

    def is_cleared(self):
        return self.left_block == self.mine_cnt

    def open(self, y, x):
        self.board[y][x].is_opened = True
        self.left_block -= 1

if __name__ == '__main__':
    SIZE = 2
    MINE = 1

    board = Board(SIZE, MINE)
    try_cnt = 0
    game_over = False

    while not game_over:
        board.print_board()
        while True:
            print(">>>", board.left_block, board.mine_cnt)
            y, x = map(int, input("(y, x)? : ").split())
            code = board.choose(y, x)
            if code == CONST.ERROR:
                continue
            elif code == CONST.BOOM:
                game_over = True
                break
            else :
                try_cnt += 1
                break
        
        if board.is_cleared():
            print("Congratulations! You win!")
            break

    print("TRY:", try_cnt)