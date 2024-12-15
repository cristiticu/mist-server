from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from context import ApplicationContext
from exceptions import register_error_handlers
from lifespan import websocket_notifications_lifespan

from routers.games import router as games_router
from routers.users import router as users_router
from routers.websocket import router as websocket_router
from routers.licenses import router as licenses_router

application_context = ApplicationContext()

app = FastAPI(title='Mist', lifespan=websocket_notifications_lifespan)

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
