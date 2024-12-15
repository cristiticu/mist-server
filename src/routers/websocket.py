from typing import Annotated
from fastapi import APIRouter, Depends, WebSocketDisconnect

from context import ApplicationContext

from notifications.connection_manager import ConnectionManager
from notifications.dependencies import connected_auth_websocket
from notifications.notifications_manager import NotificationsManager
from notifications.model import AuthWebsocket, Message, MessageBody


router = APIRouter(prefix="/ws", tags=["websocket"])

application_context = ApplicationContext()
connection_manager = ConnectionManager()
notifications_manager = NotificationsManager()


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
