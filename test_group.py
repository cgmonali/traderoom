import asyncio

from channels_redis.core import RedisChannelLayer


async def main():
    layer = RedisChannelLayer(
        hosts=["redis://127.0.0.1:6379"]
    )

    channel_name = await layer.new_channel()

    print("Channel:", channel_name)

    await layer.group_add(
        "room_1",
        channel_name,
    )

    print("GROUP ADD OK")

    await layer.group_discard(
        "room_1",
        channel_name,
    )

    print("GROUP DISCARD OK")

    await layer.flush()


asyncio.run(main())