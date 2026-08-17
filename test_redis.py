import asyncio

from channels_redis.core import RedisChannelLayer


async def main():
    layer = RedisChannelLayer(
        hosts=["redis://127.0.0.1:6379"]
    )

    channel = await layer.new_channel()

    await layer.send(
        channel,
        {
            "type": "test.message",
            "text": "hello",
        },
    )

    message = await layer.receive(channel)

    print(message)

    await layer.flush()


asyncio.run(main())