import asyncio
import json
from copy import deepcopy
from time import time

import aiohttp
import websockets


async def get_order_book_snapshot():
    uri = "https://www.binance.com/api/v3/depth?symbol=BTCUSDT&limit=100"

    async with aiohttp.ClientSession() as session:
        response = await session.get(uri)
        order_book = await response.json()
        order_book["bids"] = dict(order_book["bids"])
        order_book["asks"] = dict(order_book["asks"])
        return order_book


def update_order_book(order_book, event):
    if event["u"] <= order_book["lastUpdateId"]:
        return order_book

    order_book = deepcopy(order_book)
    order_book["lastUpdateId"] = event["u"]
    order_book["bids"].update(event["b"])
    order_book["asks"].update(event["a"])

    def filter_out_zero_quantity_levels(order_book):
        return {
            price: quantity
            for price, quantity in order_book.items()
            if float(quantity) > 0
        }

    def sort_order_book(order_book, reverse=False):
        return {
            price: quantity
            for price, quantity in sorted(
                order_book.items(), key=lambda x: float(x[0]), reverse=reverse
            )
        }

    order_book["bids"] = filter_out_zero_quantity_levels(order_book["bids"])
    order_book["asks"] = filter_out_zero_quantity_levels(order_book["asks"])

    order_book["bids"] = sort_order_book(order_book["bids"], reverse=True)
    order_book["asks"] = sort_order_book(order_book["asks"])

    return order_book


async def stream_order_book():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@depth"

    order_book = None
    events_buffer = []
    start = time()

    async with websockets.connect(uri) as websocket:
        async for event in websocket:
            event = json.loads(event)
            event["a"] = dict(event["a"])
            event["b"] = dict(event["b"])

            if not order_book:
                events_buffer.append(event)

            # buffer 5 seconds of events
            if time() - start > 5 and not order_book:
                order_book = await get_order_book_snapshot()
                for event in events_buffer:
                    order_book = update_order_book(order_book, event)
                yield order_book
                continue

            if not order_book:
                continue

            order_book = update_order_book(order_book, event)
            yield order_book


async def main():
    async for order_book in stream_order_book():
        print(order_book["lastUpdateId"])


if __name__ == "__main__":
    asyncio.run(main())
