from typing import Callable, Dict, TypeVar, Generic
from fastapi.encoders import jsonable_encoder
import json

from shared.model.entity import Entity

T = TypeVar('T', bound=Entity)


class FileRepository(Generic[T]):
    def __init__(self, *, filepath: str, persist_contents: bool = False, factory: Callable[[Dict], T]):
        self._initial_state = None
        self._filepath = filepath
        self._factory = factory
        self._persist_contents = persist_contents

    def initialize(self):
        self._initial_state = self._read_from_file()

    def destroy(self):
        if not self._persist_contents and self._initial_state is not None:
            self._write_to_file(self._initial_state)

    def _write_to_file(self, list: list[T]) -> None:
        with open(self._filepath, mode='w', encoding='utf-8') as write:
            json.dump(jsonable_encoder(list), write)

    def _read_from_file(self) -> list[T]:
        with open(self._filepath, mode='r', encoding='utf-8') as read:
            return json.load(read, object_hook=self._factory)

    def persist(self, *, entity: T) -> None:
        entities = self._read_from_file()

        try:
            index = entities.index(entity)
            entities[index] = entity
        except ValueError:
            entities.append(entity)

        self._write_to_file(entities)

    def read_all(self) -> list[T]:
        return self._read_from_file()

    def read_page(self, *, limit: int, offset: int):
        entities = self._read_from_file()

        return [entity for index, entity in enumerate(entities) if index >= offset and index - offset < limit]

    def read_many(self, *, ids: list[str]) -> list[T]:
        entities = self._read_from_file()

        return [entity for entity in entities if entity.id in ids]

    def read(self, *, id: str) -> T | None:
        entities = self._read_from_file()

        entity = [_entity for _entity in entities if _entity.id == id]

        if len(entity) == 0:
            return None

        return entity[0]

    def delete(self, *, id: str) -> None:
        entities = self._read_from_file()
        entity = self.read(id=id)

        if entity is not None:
            entities.remove(entity)
            self._write_to_file(entities)
