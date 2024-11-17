from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from shared.background_runner import BackgroundRunner
from context import ApplicationContext
from exceptions import register_error_handlers
import settings

from routers.games import router as games_router
from routers.users import router as users_router
from routers.websocket import router as websocket_router
from routers.licenses import router as licenses_router

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

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_methods=['GET', 'POST', 'DELETE', 'PATCH'],
                   allow_credentials=True,
                   allow_headers=['*']
                   )


@app.get("/", tags=["root"])
def _():
    return JSONResponse(status_code=200, content={"message": "It's Alive!"})


app.include_router(games_router)
app.include_router(users_router)
app.include_router(websocket_router)
app.include_router(licenses_router)

register_error_handlers(app)
