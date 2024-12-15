from typing import Annotated
from fastapi import APIRouter, Depends, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from context import ApplicationContext

from notifications.connection_manager import ConnectionManager
from notifications.dependencies import connected_auth_websocket
from notifications.notifications_manager import NotificationsManager
from notifications.model import AuthWebsocket


router = APIRouter(prefix="/ws", tags=["websocket"])
application_context = ApplicationContext()

connection_manager = ConnectionManager()
notifications_manager = NotificationsManager()

test_websockets_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/notification/game?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyZTFiZmMwLTVjZDEtNDQzOS04MWUzLWRhZDlhM2I0ZDdkZCIsImV4cCI6MTczNDY4NjMwNH0.uAZiI3Xqdp-1e-KQep0r2J7A_36dYpRbVL4XuPN5gzY");
            ws.onclose = (event) => {
                console.log(`Error ${event.code}, ${event.reason}, ${event.wasClean}`)
            }
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/test")
async def test_websocket():
    return HTMLResponse(test_websockets_html)


@router.websocket(path="/notification/game")
async def ws_games_notification(auth_connection: Annotated[AuthWebsocket, Depends(connected_auth_websocket)]):
    notifications_manager.subscribe(auth_connection.user_id, "games")

    try:
        while True:
            await auth_connection.websocket.receive_json()
    except WebSocketDisconnect:
        notifications_manager.withdraw_all(auth_connection.user_id)
        connection_manager.disconnect(auth_connection.user_id)


# @router.websocket(path="/notification/game")
# async def ws_games_notification(websocket: WebSocket, user: Annotated[UserTokenData, Depends(user_token_data)]):
#     await websocket.accept()

#     while True:
#         try:
#             await asyncio.wait_for(app.state.client_notification_event.wait(), 10)

#             app.state.client_notification_event.clear()

#             await websocket.send_json({"type": "notification"})
#         except TimeoutError:
#             active = await utils.is_websocket_active(websocket)
#             if not active:
#                 break
