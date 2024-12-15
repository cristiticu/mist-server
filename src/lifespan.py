import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from context import ApplicationContext
from notifications.connection_manager import ConnectionManager
from notifications.notifications_manager import NotificationsManager
import settings

notifications_manager = NotificationsManager()
connection_manager = ConnectionManager()
application_context = ApplicationContext()


@asynccontextmanager
async def websocket_notifications_lifespan(app: FastAPI):
    notman_consumer = asyncio.create_task(
        notifications_manager.consume_messages())
    _notman_test_producer = None

    if settings.START_BACKGROUND_ADDER:
        args = {"title": "Title ",
                "description": "empty",
                "price": 100,
                "positive_reviews": 0,
                "negative_reviews": 0
                }
        _notman_test_producer = asyncio.create_task(
            notifications_manager._produce_messages(channel="games", type="game_added", factory=application_context.games.create, kwargs=args))

    print("Started websocket notifications lifespan")

    yield

    notman_consumer.cancel()

    if _notman_test_producer:
        _notman_test_producer.cancel()

    await connection_manager.purge()

    print("Stopped websocket notifications lifespan")
