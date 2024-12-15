import asyncio
from typing import Callable
from notifications.connection_manager import ConnectionManager
from notifications.model import Channel, MessageType, Message, MessageBody
from users.model import UserTokenData


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
        self.subscriptions: dict[Channel, set[UserTokenData]] = dict()
        self.message_queue: asyncio.Queue[Message] = asyncio.Queue()

    def subscribe(self, user_token: UserTokenData, channel: Channel):
        if "all" not in self.subscriptions:
            self.subscriptions["all"] = set()
        self.subscriptions["all"].add(user_token)

        if channel not in self.subscriptions:
            self.subscriptions[channel] = set()
        self.subscriptions[channel].add(user_token)

    def withdraw(self, user_token: UserTokenData, channel: Channel):
        self.subscriptions["all"].discard(user_token)
        self.subscriptions[channel].discard(user_token)

    def withdraw_all(self, user_token: UserTokenData):
        for channel in self.subscriptions.keys():
            self.subscriptions[channel].discard(user_token)

    async def push_message(self, message: Message):
        await self.message_queue.put(message)

    async def consume_messages(self):
        while True:
            message = await self.message_queue.get()

            if len(self.subscriptions) > 0:
                if message.channel in self.subscriptions:
                    subscribed_connections = self.subscriptions[message.channel]
                    for token in subscribed_connections:
                        await connection_manager.send(message.body, token)
                else:
                    print(f"Warn: notifications manager got a message for inexistent channel \
                          {message.channel}")

            self.message_queue.task_done()

    async def _produce_test_messages(self, sleep_for: int = 20):
        index = 1
        while True:
            print(f"Producing message number {index}")
            body = f"Produced message number {index}"

            await self.message_queue.put(Message(channel="all", body=MessageBody(type="generic", data=body)))
            await asyncio.sleep(sleep_for)
            index += 1

    async def _produce_messages(self, *, channel: Channel, type: MessageType, factory: Callable, kwargs: dict, sleep_for: int = 20):
        index = 1
        while True:
            await asyncio.sleep(sleep_for)
            message = factory(**kwargs)
            await self.message_queue.put(Message(channel=channel, body=MessageBody(type=type, data=message)))
            index += 1
