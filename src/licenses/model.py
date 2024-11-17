from datetime import date
from shared.model.entity import Entity


class License(Entity):
    user_id: str
    game_id: str
    acquisition: date
    expires: date | None = None
    custom_image_src: str | None = None
