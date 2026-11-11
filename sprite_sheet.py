SHEET_WIDTH = 918
SHEET_HEIGHT = 506
COLUMNS = 5
ROWS = 3
FRAME_COUNT = 14

# 원본에서 각 새가 차지하는 영역. 인접 칸으로 뻗은 날개를 포함하고
# 다른 프레임의 날개 끝이 섞이지 않도록 1px 여백으로 분리했다.
# 좌표는 왼쪽 위 원점의 (left, top, right, bottom)이며 끝은 미포함이다.
FRAME_BOUNDS = (
    (33, 0, 181, 145), (215, 2, 363, 144),
    (397, 11, 545, 143), (554, 16, 727, 140),
    (728, 47, 911, 137), (33, 216, 181, 336),
    (215, 215, 363, 340), (397, 215, 545, 337),
    (579, 216, 727, 327), (761, 218, 909, 329),
    (33, 391, 181, 501), (215, 393, 363, 500),
    (375, 394, 545, 484), (545, 369, 727, 485),
)


def frame_rect(index):
    """위에서 아래, 각 행의 왼쪽부터 14장을 읽고 마지막 빈 칸은 제외한다."""
    if not 0 <= index < FRAME_COUNT:
        raise ValueError('프레임 번호는 0부터 13까지입니다')
    left, top, right, bottom = FRAME_BOUNDS[index]
    return left, SHEET_HEIGHT - bottom, right - left, bottom - top


def frame_offset(index):
    """원래 격자 중심 기준 위치를 보존해 프레임마다 크기와 중심이 튀지 않게 한다."""
    row, column = divmod(index, COLUMNS)
    left, top, right, bottom = FRAME_BOUNDS[index]
    cell_width, cell_height = SHEET_WIDTH / COLUMNS, SHEET_HEIGHT / ROWS
    dx = (left + right) / 2 - (column + 0.5) * cell_width
    dy = (row + 0.5) * cell_height - (top + bottom) / 2
    return dx, dy
