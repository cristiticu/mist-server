from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocketState

from games.persistence import GamesPersistence
from games.service import GamesService
from utils.background_runner import BackgroundRunner

import settings
import asyncio

if settings.GAMES_FILEPATH is not None:
    games = GamesPersistence(filepath=settings.GAMES_FILEPATH,
                             persist_contents=settings.PERSIST_GAMES_JSON)

    games.initialize()

    games_service = GamesService(games_persistence=games)
else:
    print('Games storage file path not found!')
    exit(-1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    background_add_task = None
    client_notification_event = asyncio.Event()

    if (settings.START_BACKGROUND_ADDER):
        background_add_task = BackgroundRunner(target=games_service.create,
                                               args={"title": "Title ",
                                                     "description": "empty",
                                                     "price": 100,
                                                     "positive_reviews": 0,
                                                     "negative_reviews": 0},
                                               sleep=20,
                                               event=client_notification_event)

    app.state.background_add_task = background_add_task
    app.state.client_notification_event = client_notification_event

    yield

    games.destroy()

    if (settings.START_BACKGROUND_ADDER and background_add_task is not None):
        background_add_task.stop()

app = FastAPI(title='Mist', lifespan=lifespan)

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['GET', 'POST', 'DELETE', 'PATCH']
                   )


@app.get("/games")
def get_users():
    return games_service.get_all()


@app.get("/games/{game_id}")
def get_user(game_id: str):
    return games_service.get(id=game_id)


@app.websocket(path="/notification/games")
async def notification_websocket(websocket: WebSocket):
    await websocket.accept()

    while True:
        await app.state.client_notification_event.wait()

        app.state.client_notification_event.clear()

        await websocket.send_text("0xAA")
