import asyncio
import threading
import time
from typing import Callable


class BackgroundRunner():
    def __init__(self, *, target: Callable, args: dict, sleep: int, event: asyncio.Event | None = None):
        self._target = target
        self._args = args
        self._sleep = sleep

        self._stop_event = threading.Event()
        self._event = event
        self._loop = asyncio.get_event_loop()

        self._thread = threading.Thread(target=self._task)
        self._thread.start()

    def _task(self):
        sleep_tick = self._sleep / 10

        time.sleep(self._sleep)

        while not self._stop_event.is_set():
            self._target(**self._args)

            if self._event:
                self._loop.call_soon_threadsafe(self._event.set)

            for _ in range(10):
                if self._stop_event.is_set():
                    break
                time.sleep(sleep_tick)

    def stop(self):
        self._stop_event.set()

        if self._thread.is_alive():
            self._thread.join()
