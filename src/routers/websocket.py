import asyncio
from fastapi import APIRouter, WebSocket

from context import ApplicationContext
from shared import utils


router = APIRouter(prefix="/ws", tags=["websocket"])
application_context = ApplicationContext()


@router.websocket(path="/notification/game")
async def ws_games_notification(websocket: WebSocket):
    await websocket.accept()

    # while True:
    #     try:
    #         await asyncio.wait_for(app.state.client_notification_event.wait(), 10)

    #         app.state.client_notification_event.clear()

    #         await websocket.send_json({"type": "notification"})
    #     except TimeoutError:
    #         active = await utils.is_websocket_active(websocket)
    #         if not active:
    #             break
