from fastapi.websockets import WebSocketState, WebSocket
import asyncio


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
