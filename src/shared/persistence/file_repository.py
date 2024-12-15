from typing import Callable, Dict, TypeVar, Generic
from fastapi.encoders import jsonable_encoder
import json

from shared.model.entity import Entity

T = TypeVar('T', bound=Entity)


class FileRepository(Generic[T]):
    def __init__(self, *, filepath: str, persist_contents: bool = False, factory: Callable[[Dict], T]):
        self._filepath = filepath
        self._factory = factory
        self._persist_contents = persist_contents

        self._database: dict[str, T] = self._read_from_file()

    def destroy(self):
        if self._persist_contents and self._database is not None:
            self._write_to_file([entity for entity in self._database.values()])

    def _write_to_file(self, list: list[T]) -> None:
        with open(self._filepath, mode='w', encoding='utf-8') as write:
            json.dump(jsonable_encoder(list), write)

    def _read_from_file(self) -> dict[str, T]:
        with open(self._filepath, mode='r', encoding='utf-8') as read:
            database = dict()
            entities = json.load(read, object_hook=self._factory)

            for entity in entities:
                database[entity.id] = entity

            return database

    def persist(self, *, entity: T) -> None:
        self._database[entity.id] = entity

    def read_all(self) -> list[T]:
        return [entity for entity in self._database.values()]

    def read_page(self, *, limit: int, offset: int):
        entities = [entity for entity in self._database.values()]
        return [entity for index, entity in enumerate(entities) if index >= offset and index - offset < limit]

    def read_many(self, *, ids: list[str]) -> list[T]:
        entities = []
        for id in ids:
            try:
                entities.append(self._database[id])
            except KeyError:
                continue

        return entities

    def read(self, *, id: str) -> T | None:
        try:
            return self._database[id]
        except KeyError:
            return None

    def delete(self, *, id: str) -> None:
        try:
            self._database.pop(id)
        except KeyError:
            return
