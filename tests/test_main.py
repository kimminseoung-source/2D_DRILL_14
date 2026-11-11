import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pico2d as p
import main
import play_mode
import game_framework
import game_world
from bird import Bird


class MainTests(unittest.TestCase):
    def test_classroom_main_pause_reset_and_exit(self):
        def key(value):
            return [SimpleNamespace(type=p.SDL_KEYDOWN, key=value, repeat=False)]
        events = [[], key(p.SDLK_p), [], key(p.SDLK_p), key(p.SDLK_r), [], key(p.SDLK_ESCAPE)]
        with patch.object(play_mode, 'get_events', side_effect=events):
            main.main()
        self.assertFalse(game_framework.running)
        self.assertEqual(game_framework.stack, [])
        self.assertTrue(all(not layer for layer in game_world.world))
        self.assertIsNone(Bird.image)
        self.assertGreater(game_framework.frame_time, 0)


if __name__ == '__main__':
    unittest.main()
