from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto
from typing import AsyncIterator

from pymongo.errors import PyMongoError

from book.config import mongo, settings


class Event(StrEnum):
    ORDERBOOK_UPDATED = auto()


@dataclass(frozen=True)
class EventInfo:
    event: str
    data: dict
    timestamp: datetime


async def emit(event: Event, data: dict):
    event_doc = {"event": event, "data": data, "timestamp": datetime.utcnow()}
    await mongo[settings.DB_NAME].events.insert_one(event_doc)


async def consume(event: Event, data_match: dict = {}) -> AsyncIterator[EventInfo]:
    collection = mongo[settings.DB_NAME].events

    def transform(data: dict):
        del data["_id"]
        return EventInfo(**data)

    match = {
        "operationType": "insert",
        "fullDocument.event": event,
        **{f"fullDocument.data.{k}": v for k, v in data_match.items()},
    }

    resume_token = None
    pipeline = [{"$match": match}]
    try:
        async with collection.watch(pipeline) as stream:
            async for insert_change in stream:
                yield transform(insert_change["fullDocument"])
                resume_token = stream.resume_token
    except PyMongoError:
        if resume_token is None:
            raise
        async with collection.watch(pipeline, resume_after=resume_token) as stream:
            async for insert_change in stream:
                yield transform(insert_change["fullDocument"])
