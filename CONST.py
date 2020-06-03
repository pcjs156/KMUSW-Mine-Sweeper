
# 배경화면 RGB 코드
BOARD_COLOR = (166, 180, 181)
BG_COLOR = (206,210,215)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# 크기관련
INNER = 10 # 게임 판의 기본 크기
CELL_SIZE = 30 # 게임에서 칸의 최소 단위
SIZE = WIDTH, HEIGHT = (2*CELL_SIZE + (INNER * CELL_SIZE)),\
                       (2*CELL_SIZE + (INNER * CELL_SIZE) + 3*CELL_SIZE) # 실제 화면에 렌더링 될 크기
FONT_SIZE = 20

# 상태 코드
ERROR = -1
DONE = 0
BOOM = 1

# 자기 자신을 포함한 순회 벡터
VECTOR = ((-1, -1), (-1, 0), (-1, 1),\
          (0, -1),  (0, 0),  (0, 1), \
          (1, -1),  (1, 0),  (1, 1))

V_DICT = {"LEFT":(0, -1), "UP":(-1, 0), "RIGHT":(0, 1), "DOWN":(1, 0)}

# 시간 관련
FPS = 60
SEC = 1000