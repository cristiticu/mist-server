from typing import Annotated
from fastapi import APIRouter, Depends, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from context import ApplicationContext

from notifications.connection_manager import ConnectionManager
from notifications.dependencies import connected_auth_websocket
from notifications.notifications_manager import NotificationsManager
from notifications.model import AuthWebsocket, Message, MessageBody


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
        <h1>Websocket Test</h1>
        <form
            action=""
            onsubmit="sendMessage(event)"
        >
            <label for="username">username</label>
            <input
                type="text"
                id="username"
                autocomplete="off"
            />
            <label for="password">password</label>
            <input
                type="text"
                id="password"
                autocomplete="off"
            />
            <button>Login</button>
        </form>
        <ul id="messages"></ul>
        <script>
            async function sendMessage(event) {
                event.preventDefault();

                const username = document.getElementById('username').value;
                const password = document.getElementById('password').value;

                const bodyFormData = new FormData();
                bodyFormData.append('username', username);
                bodyFormData.append('password', password);

                const response = await fetch('http://localhost:8000/user/auth', { method: 'POST', body: bodyFormData });
                const data = await response.json();

                console.log(data);

                const response2 = await fetch('http://localhost:8000/user', { method: 'GET', headers: { Authorization: `Bearer ${data.access_token}` } });

                var ws = new WebSocket(`ws://localhost:8000/ws/notification/game?token=${data.access_token}`);
                ws.onclose = (event) => {
                    console.log(`Error ${event.code}, ${event.reason}, ${event.wasClean}`);
                };
                ws.onmessage = function (event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };
            }
        </script>
    </body>
</html>
"""


@router.get("/test")
def test_websocket():
    return HTMLResponse(test_websockets_html)


@router.websocket(path="/notification/game")
async def ws_games_notification(auth_connection: Annotated[AuthWebsocket, Depends(connected_auth_websocket)]):
    notifications_manager.subscribe(auth_connection.user_token, "games")

    try:
        while True:
            await auth_connection.websocket.receive_json()
    except WebSocketDisconnect:
        notifications_manager.withdraw_all(auth_connection.user_token)
        connection_manager.disconnect(auth_connection.user_token)

        user = application_context.users.get(id=auth_connection.user_token.id)

        message_body = MessageBody(type="login",
                                   data=f"User {user.username} is offline")
        await notifications_manager.push_message(Message(body=message_body))


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
