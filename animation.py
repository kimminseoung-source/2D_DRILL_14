import math
from sprite_sheet import FRAME_COUNT

WINGBEATS_PER_SECOND = 5.0
CYCLE_SECONDS = 1.0 / WINGBEATS_PER_SECOND
ANIMATION_FPS = FRAME_COUNT * WINGBEATS_PER_SECOND
FRAME_SECONDS = 1.0 / ANIMATION_FPS


class WingAnimation:
    def __init__(self, phase_cycles=0.0):
        self.phase_cycles = phase_cycles % 1.0
        self.elapsed = 0.0

    def advance(self, dt):
        if not math.isfinite(dt) or dt < 0:
            raise ValueError('경과 시간은 0 이상의 유한한 값이어야 합니다')
        self.elapsed += dt

    @property
    def frame_index(self):
        position = self.elapsed * ANIMATION_FPS + self.phase_cycles * FRAME_COUNT
        # 시간 누적의 미세한 부동소수점 오차만 보정한다.
        return math.floor(position + 1e-9) % FRAME_COUNT

    @property
    def completed_cycles(self):
        return math.floor(self.elapsed * WINGBEATS_PER_SECOND + 1e-9)
