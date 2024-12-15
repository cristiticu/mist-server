from dataclasses import dataclass
from typing import Any, Literal
from fastapi import WebSocket
from pydantic import BaseModel


Channel = Literal["all", "games"]


@dataclass
class AuthWebsocket:
    websocket: WebSocket
    user_id: str


class Notification(BaseModel):
    text: str
    body: Any | None = None


class AddGameNotification(Notification):
    pass


class Message(BaseModel):
    channel: Channel
    body: Any | None = None
