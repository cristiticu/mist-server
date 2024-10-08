from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse

from games.persistence import GamesPersistence
from games.service import GamesService
from settings import GAMES_FILEPATH, PERSIST_GAMES_JSON

from utils.background_runner import BackgroundRunner
from utils.create_background_adder import create_background_adder

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

html = """
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
            var ws = new WebSocket("ws://localhost:8000/notification/games");
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


@app.get("/")
async def get():
    return HTMLResponse(html)
