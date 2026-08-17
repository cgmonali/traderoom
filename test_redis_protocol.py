import asyncio
import redis.asyncio as redis


async def main():
    r = redis.Redis(
        host="127.0.0.1",
        port=6379,
        protocol=2,
        socket_timeout=None,
    )

    print("PING:", await r.ping())
    print("Protocol 2 connection: OK")

    await r.aclose()


asyncio.run(main())