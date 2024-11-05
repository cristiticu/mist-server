from datetime import date
from uuid import uuid4
from games.model import Game
from games.persistence import GamesPersistence


class GamesService():
    def __init__(self, *, games_persistence: GamesPersistence):
        self._games = games_persistence

    def get_all(self):
        return self._games.read_all()

    def get_many(self, *, ids: list[str]):
        return self._games.read_many(ids=ids)

    def get_page(self, *, limit: int, offset: int):
        return self._games.read_page(limit=limit, offset=offset)

    def get(self, *, id: str):
        return self._games.read(id=id)

    def create(self, *, title: str,
               description: str,
               price: float,
               positive_reviews: int,
               negative_reviews: int):

        game = Game(id=str(uuid4()),
                    title=title,
                    description=description,
                    added_at=date.today(),
                    price=price,
                    positive_reviews=positive_reviews,
                    negative_reviews=negative_reviews)

        self._games.persist(entity=game)

        return game

    def delete(self, *, id: str):
        self._games.delete(id=id)
