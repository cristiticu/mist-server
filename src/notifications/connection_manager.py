from typing import Any

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from users.model import UserTokenData


class ConnectionManager():
    '''
    Manages multiple websocket connections, keeping track of users.
    '''

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.active_connections: dict[UserTokenData, WebSocket] = dict()

    def connect(self, user_token: UserTokenData, connection: WebSocket):
        self.active_connections[user_token] = connection

    def disconnect(self, user_token: UserTokenData):
        self.active_connections.pop(user_token, None)

    async def purge(self):
        for connection in self.active_connections.values():
            await connection.close(code=1011, reason="The Purge")

    async def send(self, data: Any, user_token: UserTokenData):
        encoded_data = jsonable_encoder(data)
        await self.active_connections[user_token].send_json(encoded_data)

    async def broadcast(self, data: Any):
        for connection in self.active_connections.values():
            await connection.send_json(data)
