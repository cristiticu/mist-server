from dataclasses import dataclass
from typing import Any, Literal
from fastapi import WebSocket
from pydantic import BaseModel

from users.model import UserTokenData


Channel = Literal["all", "games"]
MessageType = Literal["generic", "login", "game_added"]


@dataclass
class AuthWebsocket:
    websocket: WebSocket
    user_token: UserTokenData


class Notification(BaseModel):
    text: str
    body: Any | None = None


class AddGameNotification(Notification):
    pass


class MessageBody(BaseModel):
    type: MessageType | None = "generic"
    data: Any | None = None


class Message(BaseModel):
    channel: Channel | None = "all"
    body: MessageBody | None = None
