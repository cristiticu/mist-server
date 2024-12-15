from typing import Annotated

from fastapi import Depends, WebSocket

from notifications.connection_manager import ConnectionManager
from notifications.model import AuthWebsocket
from users.dependencies import user_token_query
from users.model import UserTokenData

connection_manager = ConnectionManager()


async def connected_auth_websocket(websocket: WebSocket, token: Annotated[UserTokenData, Depends(user_token_query)]):
    await websocket.accept()

    connection_manager.connect(token, websocket)

    return AuthWebsocket(websocket=websocket, user_token=token)
