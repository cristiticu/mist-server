from exceptions import ItemNotFound


class UserNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(UserNotFound, self).__init__(
            msg=msg or "User not found", error_trace=error_trace)
