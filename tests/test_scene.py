import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pico2d as p
import play_mode
import game_framework
import game_world
from bird import Bird


def send(key, event_type=p.SDL_KEYDOWN, repeat=False):
    event = SimpleNamespace(type=event_type, key=key, repeat=repeat)
    with patch.object(play_mode, 'get_events', return_value=[event]):
        play_mode.handle_events()


class SceneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p.open_canvas(1600, 600)

    @classmethod
    def tearDownClass(cls):
        p.close_canvas()

    def setUp(self):
        play_mode.init()
        game_framework.frame_time = 0.1
        game_framework.running = True

    def tearDown(self):
        play_mode.finish()
        game_framework.running = False

    def test_pause_resume_and_held_key(self):
        play_mode.update()
        before = [(b.x, b.animation.elapsed) for b in play_mode.birds]
        send(p.SDLK_p)
        for _ in range(5):
            play_mode.update()
        self.assertEqual(before, [(b.x, b.animation.elapsed) for b in play_mode.birds])
        send(p.SDLK_p, repeat=True)
        self.assertTrue(play_mode.paused)
        play_mode.render()
        send(p.SDLK_p)
        play_mode.update()
        self.assertAlmostEqual(play_mode.birds[0].animation.elapsed, 0.2)

    def test_reset_recreates_exactly_ten_birds(self):
        play_mode.update()
        send(p.SDLK_p)
        send(p.SDLK_r)
        self.assertEqual(len(play_mode.birds), 10)
        self.assertEqual(sum(isinstance(o, Bird) for o in game_world.world[1]), 10)
        self.assertEqual(len(game_world.world[1]), 11)
        self.assertEqual(len(game_world.world[0]), 1)
        self.assertEqual(len(game_world.world[2]), 0)
        self.assertFalse(play_mode.paused)
        self.assertTrue(all(b.animation.elapsed == 0 for b in play_mode.birds))

    def test_escape_and_window_close(self):
        for event_type, key in ((p.SDL_KEYDOWN, p.SDLK_ESCAPE), (p.SDL_QUIT, 0)):
            game_framework.running = True
            send(key, event_type)
            self.assertFalse(game_framework.running)

    def test_finish_releases_world_and_shared_texture(self):
        play_mode.finish()
        self.assertTrue(all(not layer for layer in game_world.world))
        self.assertEqual(play_mode.birds, [])
        self.assertIsNone(Bird.image)


    def test_classroom_boy_grass_ruler_and_controls_remain(self):
        from grass import Grass
        from boy import Boy
        self.assertIsInstance(game_world.world[0][0], Grass)
        self.assertIsNotNone(game_world.world[0][0].ruler_image)
        self.assertIsInstance(play_mode.boy, Boy)
        self.assertIsNotNone(play_mode.boy.font)
        self.assertTrue(all(b.y - b.DRAW_HEIGHT / 2 > 140 for b in play_mode.birds))
        before = play_mode.boy.x
        send(p.SDLK_RIGHT)
        play_mode.update()
        self.assertGreater(play_mode.boy.x, before)
        send(p.SDLK_SPACE)
        self.assertEqual(len(game_world.world[1]), 12)
        play_mode.render()


if __name__ == '__main__':
    unittest.main()
