from exceptions import CredentialsException
from users.exceptions import UserNotFound
from users.model import User
from users.persistence import UsersPersistence
from passlib.context import CryptContext


class UsersService():
    def __init__(self, *, users_persistence: UsersPersistence):
        self._users = users_persistence
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_all(self):
        return self._users.read_all()

    def get(self, *, id: str):
        user = self._users.read(id=id)

        if user is None:
            raise UserNotFound()

        return user

    def get_by_credentials(self, *, username: str, password: str):
        users = self._users.read_all()

        user = [_user for _user in users if _user.username ==
                username and self._pwd_context.verify(password, _user.password)]

        if len(user) == 0:
            raise CredentialsException()

        return user[0]
