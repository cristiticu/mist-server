import threading
import asyncio
from time import sleep

from games.service import GamesService

_stop_event = threading.Event()
_loop = asyncio.get_event_loop()


def _background_adder(service: GamesService, _add_event: asyncio.Event):
    counter = 0

    sleep(20)

    while not _stop_event.is_set():
        service.create(title="Title " + str(counter),
                       description="empty", price=float(counter), positive_reviews=0, negative_reviews=0)
        counter += 1

        _loop.call_soon_threadsafe(_add_event.set)

        for _ in range(10):
            if _stop_event.is_set():
                break
            sleep(2)


def create_background_adder(service: GamesService):
    event = asyncio.Event()

    thread = threading.Thread(target=_background_adder, args=(service, event))
    thread.start()

    return (lambda: _stop_background_adder(_thread=thread), event)


def _stop_background_adder(*, _thread: threading.Thread):
    _stop_event.set()

    if _thread.is_alive():
        _thread.join()
