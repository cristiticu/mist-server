import asyncio
from typing import Any
from notifications.connection_manager import ConnectionManager
from notifications.model import Channel, Message


connection_manager = ConnectionManager()


class NotificationsManager():
    '''
    Manages subscribed websocket connections to specific notification channels
    '''

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(NotificationsManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.subscriptions: dict[Channel, set[str]] = dict()
        self.message_queue: asyncio.Queue[Message] = asyncio.Queue()

    def subscribe(self, user_id: str, channel: Channel):
        if "all" not in self.subscriptions:
            self.subscriptions["all"] = set()
        self.subscriptions["all"].add(user_id)

        if channel not in self.subscriptions:
            self.subscriptions[channel] = set()
        self.subscriptions[channel].add(user_id)

    def withdraw(self, user_id: str, channel: Channel):
        self.subscriptions["all"].discard(user_id)
        self.subscriptions[channel].discard(user_id)

    def withdraw_all(self, user_id: str):
        for channel in self.subscriptions.keys():
            self.subscriptions[channel].discard(user_id)

    async def push_message(self, channel: Channel, body: Any):
        await self.message_queue.put(Message(channel=channel, body=body))

    async def consume_messages(self):
        while True:
            message = await self.message_queue.get()

            if len(self.subscriptions) > 0:
                if message.channel in self.subscriptions:
                    subscribed_connections = self.subscriptions[message.channel]
                    for connection in subscribed_connections:
                        await connection_manager.send(message.body, connection)
                else:
                    print(f"Warn: notifications manager got a message for inexistent channel \
                          {message.channel}")

            self.message_queue.task_done()

    async def _produce_test_messages(self, sleep_for: int = 20):
        index = 1
        while True:
            print(f"Producing message number {index}")
            body = f"Produced message number {index}"

            await self.message_queue.put(Message(channel="all", body=body))
            await asyncio.sleep(sleep_for)
            index += 1
