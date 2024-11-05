from datetime import date
from uuid import uuid4
from licenses.model import License
from licenses.persistence import LicensesPersistence


class LicensesService():
    def __init__(self, *, licenses_persistence: LicensesPersistence):
        self._licenses = licenses_persistence

    def get_all(self) -> list[License]:
        return self._licenses.read_all()

    def get(self, *, id: str):
        return self._licenses.read(id=id)

    def get_all_for_user(self, *, user_id: str):
        return [license for license in self._licenses.read_all() if license.user_id == user_id]

    def create(self, *, game_id: str, user_id: str):
        existing_licenses = self.get_all_for_user(user_id=user_id)

        existing_license = [
            _license for _license in existing_licenses if _license.game_id == game_id]

        if len(existing_license) > 0:
            return existing_license[0]

        license = License(id=str(uuid4()), user_id=user_id,
                          game_id=game_id, acquisition=date.today())

        self._licenses.persist(entity=license)

        return license
