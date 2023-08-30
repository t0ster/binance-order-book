import asyncio

import websockets


async def stream_order_book():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@depth"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print(message)
            print()


if __name__ == "__main__":
    asyncio.run(stream_order_book())
