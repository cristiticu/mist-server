from games.model import Game
from shared.persistence.file_repository import FileRepository


class GamesPersistence(FileRepository[Game]):
    def __init__(self, *, filepath: str, persist_contents: bool = False):
        super().__init__(filepath=filepath, persist_contents=persist_contents,
                         factory=lambda dict: Game(**dict))
