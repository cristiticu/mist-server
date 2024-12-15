from typing import Any

from fastapi import WebSocket


class ConnectionManager():
    '''
    Manages multiple websocket connections, keeping track of users.
    '''

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = dict()

    def connect(self, user_id: str, connection: WebSocket):
        self.active_connections[user_id] = connection

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def purge(self):
        for connection in self.active_connections.values():
            await connection.close(code=1011, reason="The Purge")

    async def send(self, data: Any, user_id: str):
        await self.active_connections[user_id].send_json(data)

    async def broadcast(self, data: Any):
        for connection in self.active_connections.values():
            await connection.send_json(data)
