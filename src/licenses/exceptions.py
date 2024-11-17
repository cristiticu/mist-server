
from exceptions import ItemNotFound


class LicenseNotFound(ItemNotFound):
    def __init__(self, msg=None, error_trace=None):
        super(LicenseNotFound, self).__init__(
            msg=msg or "License not found", error_trace=error_trace)
