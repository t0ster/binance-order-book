from copy import deepcopy
from time import time
from typing import AsyncIterator

import aiohttp

from book.domain import OrderBook
from book.events import Event, consume


async def get_order_book_snapshot(symbol: str) -> OrderBook:
    order_book = await _get_order_book_snapshot(symbol)
    return _to_entity(order_book, symbol)


def _to_entity(order_book: dict, symbol: str) -> OrderBook:
    return OrderBook.model_validate(
        {
            "symbol": symbol,
            "bids": [
                {"price": price, "size": quantity}
                for price, quantity in order_book["bids"].items()
            ],
            "asks": [
                {"price": price, "size": quantity}
                for price, quantity in order_book["asks"].items()
            ],
        }
    )


async def _get_order_book_snapshot(symbol: str) -> dict:
    _symbol = symbol.replace("/", "").upper()
    uri = f"https://www.binance.com/api/v3/depth?symbol={_symbol}&limit=500"

    async with aiohttp.ClientSession() as session:
        response = await session.get(uri)
        order_book = await response.json()
        order_book["bids"] = dict(order_book["bids"])
        order_book["asks"] = dict(order_book["asks"])
        return order_book


async def stream_order_book(symbol: str) -> AsyncIterator[OrderBook]:
    order_book = None
    events_buffer = []
    start = time()

    async for event in consume(Event.ORDERBOOK_UPDATED, {"symbol": symbol}):
        event.data["payload"]["a"] = dict(event.data["payload"]["a"])
        event.data["payload"]["b"] = dict(event.data["payload"]["b"])

        if not order_book:
            events_buffer.append(event)

        # buffer 3 seconds of events
        if time() - start > 3 and not order_book:
            order_book = await _get_order_book_snapshot(symbol)
            for event in events_buffer:
                order_book = _update_order_book(order_book, event.data["payload"])
            yield _to_entity(order_book, symbol)
            continue

        if not order_book:
            continue

        order_book = _update_order_book(order_book, event.data["payload"])
        yield _to_entity(order_book, symbol)


def _update_order_book(order_book, event: dict) -> dict:
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
