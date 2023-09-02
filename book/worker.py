import asyncio
import json

import websockets

from book.config import settings
from book.events import Event, emit


async def emit_order_book_events(symbol: str):
    _symbol = symbol.replace("/", "").lower()
    uri = f"wss://stream.binance.com:9443/ws/{_symbol}@depth"

    async with websockets.connect(uri) as websocket:  # type: ignore
        async for event_data in websocket:
            event_data = {
                "symbol": symbol,
                "payload": json.loads(event_data),
            }
            await emit(Event.ORDERBOOK_UPDATED, event_data)


async def main():
    await emit_order_book_events(settings.SYMBOL)


if __name__ == "__main__":
    asyncio.run(main())
