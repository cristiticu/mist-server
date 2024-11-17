
from exceptions import ItemNotFound


class GameNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(GameNotFound, self).__init__(
            msg=msg or "Game not found", error_trace=error_trace)
