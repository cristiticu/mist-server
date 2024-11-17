from datetime import date
from pydantic import BaseModel

from shared.model.entity import Entity


class License(Entity):
    user_id: str
    game_id: str
    acquisition: date
    expires: date | None = None
    custom_image_src: str | None = None


class LicensePatch(BaseModel):
    custom_image_src: str | None = None
