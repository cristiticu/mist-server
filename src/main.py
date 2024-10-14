from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from games.persistence import GamesPersistence
from games.service import GamesService
from utils.background_runner import BackgroundRunner

from settings import GAMES_FILEPATH, PERSIST_GAMES_JSON

if GAMES_FILEPATH is not None:
    games = GamesPersistence(filepath=GAMES_FILEPATH,
                             persist_contents=PERSIST_GAMES_JSON)

    games.initialize()

    games_service = GamesService(games_persistence=games)
else:
    print('Games storage file path not found!')
    exit(-1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    background_add_task = BackgroundRunner(target=games_service.create,
                                           args={"title": "Title ",
                                                 "description": "empty",
                                                 "price": 100,
                                                 "positive_reviews": 0,
                                                 "negative_reviews": 0},
                                           sleep=20)

    app.state.background_add_task = background_add_task

    yield

    games.destroy()
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
        await app.state.background_add_task.event.wait()

        app.state.background_add_task.event.clear()

        await websocket.send_text("0xAA")
