from threading import Thread, Event
import time

from games.service import GamesService


def _background_adder(service: GamesService, stop_event: Event):
    counter = 0

    while not stop_event.is_set():
        print('background adder adding')
        service.create(title="Title " + str(counter),
                       description="empty", price=float(counter), positive_reviews=0, negative_reviews=0)
        counter += 1

        print('background adder sleeping')
        time.sleep(10)
    print('background adder is terminating')


def create_background_adder(service: GamesService):
    print('starting background adder')
    stop_event = Event()

    thread = Thread(target=_background_adder, args=(service, stop_event))
    thread.start()

    print('started background adder')
    return lambda: _stop_background_adder(_thread=thread, _stop_event=stop_event)


def _stop_background_adder(*, _thread: Thread, _stop_event: Event):
    print('stopping background adder')
    _stop_event.set()

    if _thread is not None and type(_thread) is Thread:
        if _thread.is_alive():
            _thread.join()

    print('stopped background adder')
