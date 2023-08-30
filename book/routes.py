from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse

from book.config import settings, templates
from book.services import get_order_book_snapshot, stream_order_book

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "order-book.html", {"request": request, "symbol": settings.SYMBOL}
    )


@router.get("/stream")
async def stream_book(request: Request):
    def make_event(order_book):
        data = templates.TemplateResponse(
            "order-book.html",
            {"request": request, "order_book": order_book},
            block_name="order_book",
        )
        return {"data": data}

    async def stream():
        order_book = await get_order_book_snapshot(settings.SYMBOL)
        yield make_event(order_book)

        async for order_book in stream_order_book(settings.SYMBOL):
            yield make_event(order_book)

    return EventSourceResponse(stream())
