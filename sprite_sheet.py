SHEET_WIDTH = 918
SHEET_HEIGHT = 506
COLUMNS = 5
ROWS = 3
FRAME_COUNT = 14


def frame_rect(index):
    """위에서 아래, 각 행의 왼쪽부터 읽고 마지막 빈 칸은 제외한다."""
    if not 0 <= index < FRAME_COUNT:
        raise ValueError('프레임 번호는 0부터 13까지입니다')
    row, column = divmod(index, COLUMNS)
    left = round(column * SHEET_WIDTH / COLUMNS)
    right = round((column + 1) * SHEET_WIDTH / COLUMNS)
    top = round(row * SHEET_HEIGHT / ROWS)
    bottom = round((row + 1) * SHEET_HEIGHT / ROWS)
    # pico2d의 클리핑 원점은 이미지의 왼쪽 아래다.
    return left, SHEET_HEIGHT - bottom, right - left, bottom - top
