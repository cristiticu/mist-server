from typing import Callable, Dict, TypeVar, Generic
from fastapi.encoders import jsonable_encoder
import json

from shared.model.entity import Entity

T = TypeVar('T', bound=Entity)


class FileRepository(Generic[T]):
    def __init__(self, *, filepath: str, factory: Callable[[Dict], T]):
        self._filepath = filepath
        self._factory = factory

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

    def read(self, *, id: str) -> T:
        entities = self._read_from_file()

        entity = [_entity for _entity in entities if _entity.id == id]

        if len(entity) == 1:
            return entity[0]
        else:
            raise Exception('Entity not found')

    def delete(self, *, id: str) -> None:
        entities = self._read_from_file()
        entity = self.read(id=id)

        entities.remove(entity)
        self._write_to_file(entities)
