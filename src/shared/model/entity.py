from pydantic import BaseModel


class Entity(BaseModel):
    id: str

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Entity):
            return self.id == other.id
        return False
