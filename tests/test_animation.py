import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from animation import WingAnimation, ANIMATION_FPS, CYCLE_SECONDS, FRAME_SECONDS


class AnimationTests(unittest.TestCase):
    def test_exact_14_frame_sequence_and_wrap(self):
        animation = WingAnimation()
        frames = []
        for _ in range(14):
            frames.append(animation.frame_index)
            animation.advance(FRAME_SECONDS)
        self.assertEqual(frames, list(range(14)))
        self.assertEqual(animation.frame_index, 0)
        self.assertEqual(animation.completed_cycles, 1)

    def test_five_cycles_per_second(self):
        animation = WingAnimation()
        animation.advance(1.0)
        self.assertEqual(animation.completed_cycles, 5)
        self.assertEqual(animation.frame_index, 0)
        self.assertEqual(ANIMATION_FPS, 70.0)
        self.assertEqual(CYCLE_SECONDS, 0.2)

    def test_invalid_time_is_rejected(self):
        for dt in (-1, float('nan'), float('inf')):
            with self.assertRaises(ValueError):
                WingAnimation().advance(dt)


if __name__ == '__main__':
    unittest.main()
