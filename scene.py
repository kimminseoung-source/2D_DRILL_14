from pico2d import load_image, load_font, get_canvas_width, get_canvas_height
from resources import asset
from animation import ANIMATION_FPS, WINGBEATS_PER_SECOND
from sprite_sheet import FRAME_COUNT
import game_framework


class Sky:
    def __init__(self):
        self.image = load_image(asset('sky.png'))

    def update(self):
        pass

    def draw(self):
        width, height = get_canvas_width(), get_canvas_height()
        self.image.draw(width / 2, height / 2, width, height)


class HUD:
    def __init__(self, birds):
        self.birds = birds
        self.font = load_font(asset('ENCR10B.TTF'), 18)
        self.title_font = load_font(asset('ENCR10B.TTF'), 26)
        self.paused = False

    def update(self):
        pass

    def draw(self):
        height = get_canvas_height()
        self.title_font.draw(30, height - 33, 'DRILL 14 | TEN BIRDS IN FLIGHT', (242, 250, 255))
        self.font.draw(30, height - 65,
                       f'{FRAME_COUNT} frames/cycle x {WINGBEATS_PER_SECOND:.0f} cycles/s = {ANIMATION_FPS:.0f} animation frames/s',
                       (133, 226, 225))
        elapsed = self.birds[0].animation.elapsed
        self.font.draw(30, height - 90,
                       f'Birds: {len(self.birds)} | Simulation: {elapsed:.2f}s | Render FPS: {game_framework.frame_rate:.1f}',
                       (225, 235, 245))
        self.font.draw(30, 10, 'P: pause / resume    R: reset    ESC: quit', (35, 65, 80))
        for bird in self.birds:
            self.font.draw(bird.x - 20, bird.y - 75, f'{bird.number:02d}', (35, 65, 85))
        if self.paused:
            self.title_font.draw(get_canvas_width() / 2 - 100, height / 2, 'PAUSED', (25, 45, 65))
