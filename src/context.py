from games.persistence import GamesPersistence
from games.service import GamesService
from licenses.persistence import LicensesPersistence
from licenses.service import LicensesService
from users.persistence import UsersPersistence
from users.service import UsersService
import settings


class ApplicationContext():
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ApplicationContext, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if settings.GAMES_FILEPATH is None:
            print('Games storage file path not found!')
            exit(-1)
        if settings.USERS_FILEPATH is None:
            print('Users storage file path not found!')
            exit(-1)
        if settings.LICENSES_FILEPATH is None:
            print('Licenses storage file path not found!')
            exit(-1)

        self._games_persistence = GamesPersistence(filepath=settings.GAMES_FILEPATH,
                                                   persist_contents=settings.PERSIST_GAMES_JSON)
        self.games = GamesService(
            games_persistence=self._games_persistence)

        self._users_persistence = UsersPersistence(
            filepath=settings.USERS_FILEPATH, persist_contents=settings.PERSIST_USERS_JSON)

        self.users = UsersService(users_persistence=self._users_persistence)

        self._licenses_persistence = LicensesPersistence(filepath=settings.LICENSES_FILEPATH,
                                                         persist_contents=settings.PERSIST_LICENSES_JSON)

        self.licenses = LicensesService(
            licenses_persistence=self._licenses_persistence)

    def destroy(self):
        self._games_persistence.destroy()
        self._users_persistence.destroy()
        self._licenses_persistence.destroy()
