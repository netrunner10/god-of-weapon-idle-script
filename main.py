import time
import threading

from pynput.keyboard import Controller, Listener, Key

WARMUP_TIME = 1
WORK_TIME = 60 * 10
WASD_DELAY_TIME = 4
SPACE_DELAY_TIME = 1
THREAD_TIMEOUT_TIME = .1
KEYS_TO_PRESS = ("d", "w", "a", "s",)

run_monitor = threading.Event()
finish_monitor = threading.Event()

def press_dwas(keyboard: Controller):
    while True:
        run_monitor.wait()

        if finish_monitor.is_set():
            break

        for key in KEYS_TO_PRESS:
            print(f"Pressing `{key.upper()}`...")
            keyboard.press(key)
            time.sleep(WASD_DELAY_TIME)
            keyboard.release(key)

def tap_space(keyboard: Controller):
    while True:
        run_monitor.wait()

        if finish_monitor.is_set():
            break

        print("Tapping `SPACE`...")
        keyboard.tap(Key.space)
        time.sleep(SPACE_DELAY_TIME)


def pause(key):
    if key == Key.tab:
        if run_monitor.is_set():
            run_monitor.clear()

            for i in range(3):
                print(f"Pausing in `{3-i}` sec...")
                time.sleep(1)

            print("Paused")

        else:
            for i in range(3):
                print(f"Starting in `{3-i}`...")
                time.sleep(1)

            run_monitor.set()
            print("Go!")

def start():
    keyboard = Controller()
    listener = Listener(on_press=pause)
    dwas_thread = threading.Thread(target=press_dwas, args=(keyboard,))
    space_thread = threading.Thread(target=tap_space, args=(keyboard,))

    run_monitor.set()

    print(f"App is initialized. Wait for {WARMUP_TIME} sec. to start.")
    time.sleep(WARMUP_TIME)

    listener.start()
    dwas_thread.start()
    space_thread.start()

    time.sleep(WORK_TIME)
    finish_monitor.set()

    space_thread.join(timeout=THREAD_TIMEOUT_TIME)
    dwas_thread.join(timeout=THREAD_TIMEOUT_TIME)
    listener.join(timeout=THREAD_TIMEOUT_TIME)


if __name__ == "__main__":
    start()
