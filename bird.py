from pico2d import load_image
from resources import asset
from sprite_sheet import frame_rect
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

    def draw(self):
        x, y, width, height = frame_rect(self.animation.frame_index)
        flip = '' if self.direction > 0 else 'h'
        Bird.image.clip_composite_draw(
            x, y, width, height, 0, flip,
            self.x, self.y, self.DRAW_WIDTH, self.DRAW_HEIGHT
        )
