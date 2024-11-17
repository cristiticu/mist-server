from datetime import datetime, timedelta, timezone
from fastapi.websockets import WebSocketState, WebSocket
import jwt
import asyncio
import settings


async def is_websocket_active(websocket: WebSocket) -> bool:
    if not (websocket.application_state == WebSocketState.CONNECTED and websocket.client_state == WebSocketState.CONNECTED):
        return False
    try:
        await asyncio.wait_for(websocket.send_json({"type": "heartbeat"}), 5)
        message = await asyncio.wait_for(websocket.receive_json(), 5)
        assert message["type"] == "heartbeat"
    except BaseException:
        return False
    return True


def create_access_token(data: dict, expire=settings.ACCESS_TOKEN_EXPIRE_MINUTES):
    expire_delta = timedelta(expire)
    encode = data.copy()
    expires_at = datetime.now(timezone.utc) + expire_delta
    encode.update({"exp": expires_at})

    return jwt.encode(encode, settings.SECRET_KEY, settings.ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
