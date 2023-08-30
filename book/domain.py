from decimal import Decimal

from pydantic import BaseModel


class PriceLevel(BaseModel):
    price: Decimal
    size: Decimal


class OrderBook(BaseModel):
    bids: list[PriceLevel]
    asks: list[PriceLevel]
