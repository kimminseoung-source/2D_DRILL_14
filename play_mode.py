from pico2d import *
import game_world
import game_framework
from bird import Bird
from scene import Sky, HUD

birds = []
hud = None
paused = False


def handle_events():
    global paused
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
            return
        elif event.type == SDL_KEYDOWN and not getattr(event, 'repeat', False):
            if event.key == SDLK_p:
                paused = not paused
                hud.paused = paused
            elif event.key == SDLK_r:
                init()
                return


def init():
    global birds, hud, paused
    paused = False
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
    global paused
    paused = True
    hud.paused = True


def resume():
    global paused
    paused = False
    hud.paused = False


def finish():
    global birds, hud, paused
    game_world.clear()
    birds = []
    hud = None
    paused = False
    Bird.image = None


def update():
    if not paused:
        game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
