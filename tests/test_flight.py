import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bird import Bird
from sprite_sheet import frame_rect, FRAME_COUNT, SHEET_WIDTH, SHEET_HEIGHT


class FlightTests(unittest.TestCase):
    def setUp(self):
        self.image_patch = patch.object(Bird, 'image', object())
        self.image_patch.start()

    def tearDown(self):
        self.image_patch.stop()

    def test_flight_matches_across_fps_and_reflections(self):
        results = []
        for fps in (20, 30, 60, 120, 144):
            bird = Bird(1, 400, 200, speed=137, direction=-1)
            for _ in range(fps * 10):
                bird.update(1 / fps, 1600)
            results.append((bird.x, bird.direction, bird.animation.completed_cycles))
        for x, direction, cycles in results:
            self.assertAlmostEqual(x, results[0][0])
            self.assertEqual(direction, results[0][1])
            self.assertEqual(cycles, 50)

    def test_large_delta_does_not_leave_window(self):
        bird = Bird(1, 80, 200, speed=200, direction=-1)
        bird.update(100.0, 1600)
        self.assertTrue(60 <= bird.x <= 1540)
        self.assertEqual(bird.animation.completed_cycles, 500)

    def test_ten_independent_clocks_and_one_texture(self):
        birds = [Bird(i+1, 200+i*100, 200, phase_cycles=i/10) for i in range(10)]
        self.assertEqual(len({id(b.animation) for b in birds}), 10)
        self.assertEqual(len({id(b.image) for b in birds}), 1)
        for bird in birds:
            bird.update(1.0, 1600)
            self.assertEqual(bird.animation.completed_cycles, 5)

    def test_all_frame_rectangles_and_unused_cell(self):
        rectangles = [frame_rect(i) for i in range(FRAME_COUNT)]
        self.assertEqual(len(set(rectangles)), 14)
        for x, y, w, h in rectangles:
            self.assertTrue(0 <= x < x+w <= SHEET_WIDTH)
            self.assertTrue(0 <= y < y+h <= SHEET_HEIGHT)
        with self.assertRaises(ValueError):
            frame_rect(14)


if __name__ == '__main__':
    unittest.main()
