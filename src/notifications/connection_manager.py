from typing import Any
from uuid import uuid4

from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder

from notifications.model import AuthWebsocket
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
        self.active_connections: dict[str, AuthWebsocket] = dict()

    def connect(self, user_token: UserTokenData, connection: WebSocket):
        auth_websocket = AuthWebsocket(
            id=str(uuid4()), websocket=connection, user_token=user_token)

        self.active_connections[auth_websocket.id] = auth_websocket

        return auth_websocket

    def disconnect(self, connection_id: str):
        self.active_connections.pop(connection_id, None)

    async def purge(self):
        for connection in self.active_connections.values():
            await connection.websocket.close(code=1011, reason="The Purge")

    async def send(self, data: Any, connection_id: str):
        encoded_data = jsonable_encoder(data)
        await self.active_connections[connection_id].websocket.send_json(encoded_data)

    async def broadcast(self, data: Any):
        for connection in self.active_connections.values():
            await connection.websocket.send_json(data)
