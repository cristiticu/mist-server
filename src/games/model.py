from datetime import date
from shared.model.entity import Entity


class Game(Entity):
    title: str
    description: str
    price: float
    added_at: date
    positive_reviews: int
    negative_reviews: int
