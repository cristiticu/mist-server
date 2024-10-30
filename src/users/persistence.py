from shared.persistence.file_repository import FileRepository
from users.model import User


class UsersPersistence(FileRepository[User]):
    def __init__(self, *, filepath: str, persist_contents: bool = False):
        super().__init__(filepath=filepath, persist_contents=persist_contents,
                         factory=lambda dict: User(**dict))
