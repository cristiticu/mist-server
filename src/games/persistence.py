from games.model import Game
from shared.persistence.file_repository import FileRepository


class GamesPersistence(FileRepository[Game]):
    def __init__(self, *, filepath: str):
        super().__init__(filepath=filepath, factory=lambda dict: Game(**dict))
