from pico2d import load_image, get_canvas_width
import game_framework
from resources import asset
from sprite_sheet import frame_rect, frame_offset, SHEET_WIDTH, SHEET_HEIGHT, COLUMNS, ROWS
from animation import WingAnimation


class Bird:
    image = None
    DRAW_WIDTH = 120
    DRAW_HEIGHT = 110

    def __init__(self, number, x, y, speed=90.0, direction=1, phase_cycles=0.0):
        if Bird.image is None:
            Bird.image = load_image(asset('bird_animation.png'))
        self.number = number
        self.x, self.y = x, y
        self.speed = speed
        self.direction = direction
        self.animation = WingAnimation(phase_cycles)

    def update(self, dt=None, canvas_width=None):
        if dt is None:
            dt = game_framework.frame_time
        if canvas_width is None:
            canvas_width = get_canvas_width()
        self.animation.advance(dt)
        left = self.DRAW_WIDTH / 2
        span = canvas_width - self.DRAW_WIDTH
        if span <= 0:
            raise ValueError('창 너비는 새의 너비보다 커야 합니다')
        offset = self.x - left
        unfolded = offset if self.direction > 0 else 2 * span - offset
        phase = (unfolded + self.speed * dt) % (2 * span)
        if phase < span:
            self.x = left + phase
            self.direction = 1
        else:
            self.x = left + 2 * span - phase
            self.direction = -1

    def draw(self):
        index = self.animation.frame_index
        x, y, width, height = frame_rect(index)
        dx, dy = frame_offset(index)
        scale_x = self.DRAW_WIDTH / (SHEET_WIDTH / COLUMNS)
        scale_y = self.DRAW_HEIGHT / (SHEET_HEIGHT / ROWS)
        flip = '' if self.direction > 0 else 'h'
        if self.direction < 0:
            dx = -dx
        Bird.image.clip_composite_draw(
            x, y, width, height, 0, flip,
            self.x + dx * scale_x, self.y + dy * scale_y,
            width * scale_x, height * scale_y
        )
