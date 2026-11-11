from pico2d import *
import game_world
import game_framework
from bird import Bird
from scene import Sky, HUD

birds = []
hud = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            return


def init():
    global birds, hud
    game_world.clear()
    width = get_canvas_width()
    birds = [
        Bird(i + 1,
             width * ((i % 5) + 0.5) / 5,
             190 + (i // 5) * 220,
             speed=75.0 + i * 7.0,
             direction=1 if i % 2 == 0 else -1,
             phase_cycles=i / 10.0)
        for i in range(10)
    ]
    game_world.add_oject(Sky(), 0)
    for bird in birds:
        game_world.add_oject(bird)
    hud = HUD(birds)
    game_world.add_oject(hud, 2)


def pause():
    pass


def resume():
    pass


def finish():
    global birds, hud
    game_world.clear()
    birds = []
    hud = None
    Bird.image = None


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
