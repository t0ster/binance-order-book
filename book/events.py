from dataclasses import asdict, dataclass, field
from datetime import datetime

from pymongo.errors import PyMongoError

from book.config import mongo, settings


@dataclass(frozen=True)
class Event:
    event: str
    data: dict
    timestamp: datetime = field(default_factory=datetime.utcnow)


async def emit(event: Event):
    await mongo[settings.DB_NAME].events.insert_one(asdict(event))


async def consume(event_name: str, data_match: dict = {}):
    collection = mongo[settings.DB_NAME].events

    def transform(data: dict):
        del data["_id"]
        return Event(**data)

    match = {
        "operationType": "insert",
        "fullDocument.event": event_name,
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
