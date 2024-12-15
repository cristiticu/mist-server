from typing import Annotated

from fastapi import Depends, WebSocket

from notifications.connection_manager import ConnectionManager
from users.dependencies import user_token_query
from users.model import UserTokenData

connection_manager = ConnectionManager()


async def connected_auth_websocket(websocket: WebSocket, token: Annotated[UserTokenData, Depends(user_token_query)]):
    await websocket.accept()
    return connection_manager.connect(token, websocket)
