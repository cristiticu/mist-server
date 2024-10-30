from contextlib import asynccontextmanager
import asyncio
from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from jwt import InvalidTokenError

from context import ApplicationContext
import settings
import shared.utils as utils
from shared.background_runner import BackgroundRunner

application_context = ApplicationContext()


@asynccontextmanager
async def lifespan(app: FastAPI):
    background_add_task = None
    client_notification_event = asyncio.Event()

    if (settings.START_BACKGROUND_ADDER):
        background_add_task = BackgroundRunner(target=application_context.games.create,
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

    application_context.destroy()

    if (settings.START_BACKGROUND_ADDER and background_add_task is not None):
        background_add_task.stop()

app = FastAPI(title='Mist', lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['GET', 'POST', 'DELETE', 'PATCH']
                   )


# Public Routes


@app.post("/auth/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]):
    user = application_context.users.get_by_credentials(
        username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = utils.create_access_token({"id": user.id}, timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    return {
        "access_token": token, "token_type": "bearer"
    }


@app.get("/games")
def get_all_games():
    return application_context.games.get_all()


@app.get("/games/{game_id}")
def get_game(game_id: str):
    game = application_context.games.get(id=game_id)

    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )

    return game

# Private Routes


@app.get("/user/my-games")
def get_user_games(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = utils.decode_access_token(token)
        user_id = payload.get("id")

        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    licenses = application_context.licenses.get_all_for_user(user_id=user_id)
    games_ids = [license.game_id for license in licenses]

    return application_context.games.get_many(ids=games_ids)


@app.websocket(path="/notification/games")
async def ws_games_notification(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            await asyncio.wait_for(app.state.client_notification_event.wait(), 10)

            app.state.client_notification_event.clear()

            await websocket.send_json({"type": "notification"})
        except TimeoutError:
            active = await utils.is_websocket_active(websocket)
            if not active:
                break
