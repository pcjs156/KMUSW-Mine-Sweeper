import pygame as pygame
from random import randint

import CONST
from elements import *
from player import Player

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

        # board_gui : 플레이어가 보게 될 보드(렌더링 기준)
        self.board_gui = [[False for _ in range(self.size)] for _ in range(self.size)]
                    
        # 플레이어 인스턴스 생성
        # player1 : p[1] | player2 : p[2]
        # 플레이어 1이 먼저 게임을 시작하고, play()의 마지막에 순서를 넘김
        self.p = {1:Player(self.size), 2:Player(self.size)}
        self.now = 1

    def main(self):
        while True :
            if self.play() is False :
                winner, loser = self.get_winner_loser()
                break
        print("WINNER : PLAYER {}".format(winner))
        print("LOSER : PLAYER {}".format(loser))

    def play(self):
        print("PLAYER {}'s TURN".format(self.now))
        player_now = self.p[self.now]
        
        while True:
            self.print_board()
            print("남은 블럭 수 :", self.left_block)
            y, x = map(int, input("(y, x)? : ").split())
            code = board.choose(y, x)
            if code == CONST.ERROR:
                continue
            elif code == CONST.BOOM:
                player_now.is_game_over = True
                break
            else :
                player_now.try_cnt += 1
                break
        
        # 만약 player_now가 졌으면
        # 게임이 끝났다는 의미로 False를 리턴해 main 메서드에 전달
        if player_now.is_game_over is True:
            return False

        # 만약 게임이 안끝났다면 True를 리턴해 main 메서드에 전달
        else :
            # 1플레이어의 차례였으면 2플레이어로,
            # 2플레이어의 차례였으면 1플레이어로
            self.change_player()
            return True
    
    def play_gui(self, y, x):
        player_now = self.p[self.now]
        
        if not self.board[y][x].is_opened:
            code = board.choose(y, x)
            if code == CONST.BOOM:
                player_now.is_game_over = True
            else :
                player_now.try_cnt += 1
        
        if player_now.is_game_over is True:
            return False

        else :
            self.change_player()
            return True
    
    def change_player(self):
        if self.now == 1 : self.now = 2
        else : self.now = 1

    def get_winner_loser(self):
        # 1이 졌으면 (2, 1), 2가 졌으면(1, 2) 리턴 [(승자, 패자)]
        return (2, 1) if self.p[1].is_game_over is True else (1, 2)


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
                self.open_chaining(y, x)


    def open_chaining(self, y, x):
        
        if isinstance(self.board[y][x], Wall) or (self.board[y][x].is_opened is True) :
            return

        self.p[self.now].score += 1
        self.board[y][x].is_opened = True
        self.left_block -= 1

        mine_around = False
        
        for v in CONST.VECTOR:
            if isinstance(self.board[y+v[0]][x+v[1]], Mine) :
                mine_around = True
                break

        if mine_around :
            return
        else :
            for v in CONST.VECTOR:
                self.open_chaining(y+v[0], x+v[1])   

    def is_cleared(self):
        return self.left_block == self.mine_cnt


if __name__ == '__main__':
    SIZE = 5
    MINE = 10

    board = Board(SIZE, MINE)
    board.main()