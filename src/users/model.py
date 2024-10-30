from datetime import date
from shared.model.entity import Entity


class User(Entity):
    username: str
    password: str
    created_at: date
    profile_img: str | None = None
