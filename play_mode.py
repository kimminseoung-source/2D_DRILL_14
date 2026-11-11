from pico2d import *
import game_world
import game_framework
from bird import Bird
from boy import Boy
from ball import Ball
from grass import Grass
from resources import asset

birds = []
boy = None
font = None
paused = False
pause_started_at = 0.0


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
                return
            if event.key == SDLK_p:
                if not getattr(event, 'repeat', False):
                    resume() if paused else pause()
                continue
            if event.key == SDLK_r:
                if not getattr(event, 'repeat', False):
                    init()
                return
        if not paused:
            boy.handle_event(event)
        elif event.type == SDL_KEYUP:
            boy.pressed_keys.discard(event.key)


def init():
    global birds, boy, font, paused
    paused = False
    game_world.clear()
    boy = Boy()
    game_world.add_oject(Grass(), 0)
    game_world.add_oject(boy)
    font = load_font(asset('ENCR10B.TTF'), 16)
    width = get_canvas_width()
    birds = [
        Bird(i + 1,
             width * ((i % 5) + 0.5) / 5,
             230 + (i // 5) * 240,
             speed=75.0 + i * 7.0,
             direction=1 if i % 2 == 0 else -1,
             phase_cycles=i / 10.0)
        for i in range(10)
    ]
    for bird in birds:
        game_world.add_oject(bird)


def pause():
    global paused, pause_started_at
    if not paused:
        paused = True
        pause_started_at = get_time()
        boy.pause()


def resume():
    global paused
    if paused:
        boy.idle_started_at += get_time() - pause_started_at
        paused = False


def finish():
    global birds, boy, font, paused
    game_world.clear()
    birds = []
    boy = None
    font = None
    paused = False
    Bird.image = None
    Ball.images.clear()


def update():
    if not paused:
        game_world.update()


def render():
    clear_canvas()
    game_world.render()
    font.draw(20, get_canvas_height() - 25,
              '10 BIRDS | 14 frames x 5 cycles/s = 70 animation FPS | P: pause R: reset ESC: quit',
              (30, 60, 90))
    if paused:
        font.draw(get_canvas_width() / 2 - 40, get_canvas_height() / 2 + 45,
                  'PAUSED', (30, 60, 90))
    update_canvas()
