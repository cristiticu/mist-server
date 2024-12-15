import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from notifications.connection_manager import ConnectionManager
from notifications.notifications_manager import NotificationsManager
import settings

notifications_manager = NotificationsManager()
connection_manager = ConnectionManager()


@asynccontextmanager
async def websocket_notifications_lifespan(app: FastAPI):
    notman_consumer = asyncio.create_task(
        notifications_manager.consume_messages())
    _notman_test_producer = None

    if settings.START_BACKGROUND_ADDER:
        _notman_test_producer = asyncio.create_task(
            notifications_manager._produce_test_messages())

    print("Started websocket notifications lifespan")

    yield

    notman_consumer.cancel()

    if _notman_test_producer:
        _notman_test_producer.cancel()

    await connection_manager.purge()

    print("Stopped websocket notifications lifespan")


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     background_add_task = None
#     client_notification_event = asyncio.Event()

#     if (settings.START_BACKGROUND_ADDER):
#         background_add_task = BackgroundRunner(target=application_context.games.create,
#                                                args={"title": "Title ",
#                                                      "description": "empty",
#                                                      "price": 100,
#                                                      "positive_reviews": 0,
#                                                      "negative_reviews": 0},
#                                                sleep=20,
#                                                event=client_notification_event)

#     app.state.background_add_task = background_add_task
#     app.state.client_notification_event = client_notification_event

#     yield

#     application_context.destroy()

#     if (settings.START_BACKGROUND_ADDER and background_add_task is not None):
#         background_add_task.stop()
