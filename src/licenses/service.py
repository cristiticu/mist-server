from licenses.model import License
from licenses.persistence import LicensesPersistence


class LicensesService():
    def __init__(self, *, licenses_persistence: LicensesPersistence):
        self._licenses = licenses_persistence

    def get_all(self) -> list[License]:
        return self._licenses.read_all()

    def get(self, *, id: str) -> License:
        return self._licenses.read(id=id)

    def get_all_for_user(self, *, user_id: str) -> list[License]:
        return [license for license in self._licenses.read_all() if license.user_id == user_id]
