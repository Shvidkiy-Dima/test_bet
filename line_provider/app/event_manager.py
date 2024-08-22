import asyncio
import json

from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustChannel, AbstractRobustConnection
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from loguru import logger
from settings import settings


class EventManager:
    TASK = None
    connection: AbstractRobustConnection
    channel: AbstractRobustChannel
    callback_client: AsyncClient = AsyncClient()

    @classmethod
    async def start(cls):
        cls.TASK = asyncio.create_task(cls.consume())

    @classmethod
    async def stop(cls):
        await cls.connection.close()
        await cls.callback_client.aclose()

    @classmethod
    async def consume(cls):
        logger.info('START CONSUME')
        cls.connection = await connect_robust(
            host=settings.MQ_HOST, port=settings.MQ_PORT, login=settings.MQ_USER, password=settings.MQ_PASS
        )

        cls.channel = await cls.connection.channel()

        queue = await cls.channel.declare_queue(settings.QUEUE_NAME)

        await queue.consume(callback=cls.on_event, no_ack=False)

    @classmethod
    async def put_event(cls, message: dict):
        logger.info('RECEIVE NEW EVENT')
        message = json.dumps(jsonable_encoder(message)).encode()
        await cls.channel.default_exchange.publish(
            Message(message),
            routing_key=settings.QUEUE_NAME,
        )

    @classmethod
    async def on_event(cls, message: AbstractIncomingMessage):
        async with message.process(ignore_processed=True):
            try:
                message_body = message.body
                message_body_json = json.loads(message_body.decode())
                res = await cls.callback_client.post(url=settings.BET_MAKER_CALLBACK_URL, json=message_body_json)
                res.raise_for_status()
                await message.ack()
                logger.info(f"SEND EVENT SUCCESS {message_body_json}")
            except Exception as e:
                logger.info(f"SEND EVENT ERROR {e}")
                await message.nack(requeue=True)
