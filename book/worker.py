import asyncio
import json

import websockets

from book.config import settings
from book.events import Event, emit


async def emit_order_book_events(symbol: str):
    _symbol = symbol.replace("/", "").lower()
    uri = f"wss://stream.binance.com:9443/ws/{_symbol}@depth"

    async with websockets.connect(uri) as websocket:  # type: ignore
        async for event in websocket:
            event = json.loads(event)
            event = Event(
                event="orderbook_updated",
                data={"symbol": symbol, "payload": event},
            )
            await emit(event)


async def main():
    await emit_order_book_events(settings.SYMBOL)


if __name__ == "__main__":
    asyncio.run(main())
