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


    def test_same_ten_second_result_at_different_game_fps(self):
        for fps in (20, 30, 60, 120, 144):
            with self.subTest(fps=fps):
                animation = WingAnimation(phase_cycles=0.3)
                start = animation.frame_index
                for _ in range(fps * 10):
                    animation.advance(1.0 / fps)
                self.assertAlmostEqual(animation.elapsed, 10.0)
                self.assertEqual(animation.completed_cycles, 50)
                self.assertEqual(animation.frame_index, start)

    def test_irregular_and_large_frame_intervals_keep_phase(self):
        animation = WingAnimation()
        for dt in (0.01, 0.09, 0.37, 0.03, 0.5):
            animation.advance(dt)
            self.assertTrue(0 <= animation.frame_index < 14)
        self.assertEqual(animation.completed_cycles, 5)
        self.assertEqual(animation.frame_index, 0)
        animation.advance(0.5)
        self.assertEqual(animation.completed_cycles, 7)
        self.assertEqual(animation.frame_index, 7)

    def test_initial_phase_changes_pose_but_not_frequency(self):
        for i in range(10):
            animation = WingAnimation(i / 10)
            start = animation.frame_index
            animation.advance(1.0)
            self.assertEqual(animation.frame_index, start)
            self.assertEqual(animation.completed_cycles, 5)


if __name__ == '__main__':
    unittest.main()
