from datetime import date

from pydantic import BaseModel
from shared.model.entity import Entity


class User(Entity):
    username: str
    password: str
    created_at: date
    profile_img: str | None = None


class UserTokenData(BaseModel):
    id: str
