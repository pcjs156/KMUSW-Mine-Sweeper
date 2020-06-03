
# 배경화면 RGB 코드
BOARD_COLOR = (166, 180, 181)
BG_COLOR = (206,210,215)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 게임 판의 기본 크기
INNER = 10
CELL_SIZE = 30
SIZE = WIDTH, HEIGHT = (2*CELL_SIZE + (INNER * CELL_SIZE)),\
                       (2*CELL_SIZE + (INNER * CELL_SIZE) + 3*CELL_SIZE)

# 상태 코드
ERROR = -1
DONE = 0
BOOM = 1

# 자기 자신을 포함한 순회 벡터
VECTOR = ((-1, -1), (-1, 0), (-1, 1),\
          (0, -1),  (0, 0),  (0, 1), \
          (1, -1),  (1, 0),  (1, 1))

# 시간 관련
FPS = 60
SEC = 1000