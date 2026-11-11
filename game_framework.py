import time
running = False
stack = []


def change_mode(mode):
    if stack:
        stack.pop().finish()
    stack.append(mode)
    mode.init()


def push_mode(mode):
    if stack:
        stack[-1].pause()
    stack.append(mode)
    mode.init()


def pop_mode():
    if stack:
        stack.pop().finish()
    if stack:
        stack[-1].resume()
    else:
        quit()


def quit():
    global running
    running = False

frame_time = 0.0
frame_rate = 0.0
TARGET_FPS = 120.0

def run(start_mode):
    global running, stack
    running = True
    stack = [start_mode]
    try:
        start_mode.init()

        global frame_time, frame_rate
        frame_time = 0.0
        frame_rate = 0.0
        current_time = time.perf_counter()  # 시스템 시각 보정에 영향받지 않는 경과 시간

        while running:
            
            stack[-1].handle_events()
            if not running:
                break
            stack[-1].update()
            if not running:
                break
            stack[-1].render()

            remaining = 1.0 / TARGET_FPS - (time.perf_counter() - current_time)
            if remaining > 0:
                time.sleep(remaining)
            now = time.perf_counter()
            frame_time = now - current_time
            frame_rate = 1.0 / frame_time if frame_time > 0 else 0.0
            current_time = now
            # print(f'Frame Time:{frame_time}, Frame Rate:{frame_rate}')

    finally:
        while stack:
            stack.pop().finish()
        running = False
