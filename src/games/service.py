from datetime import date
from uuid import uuid4
from games.model import Game
from games.persistence import GamesPersistence


class GamesService():
    def __init__(self, *, games_persistence: GamesPersistence):
        self._games = games_persistence

    def get_all(self) -> list[Game]:
        return self._games.read_all()

    def get(self, *, id: str) -> Game:
        return self._games.read(id=id)

    def create(self, *, title: str,
               description: str,
               price: float,
               positive_reviews: int,
               negative_reviews: int) -> Game:

        game = Game(id=str(uuid4()),
                    title=title,
                    description=description,
                    added_at=date.today(),
                    price=price,
                    positive_reviews=positive_reviews,
                    negative_reviews=negative_reviews)

        self._games.persist(entity=game)

        return game

    def delete(self, *, id: str) -> None:
        self._games.delete(id=id)
