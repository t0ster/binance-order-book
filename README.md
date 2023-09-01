# README

## Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2 templates](https://jinja.palletsprojects.com/en/3.1.x/)
- [HTMX](https://htmx.org/)
- MongoDB

## Features and Limitations

- Uses [server-sent events](https://en.wikipedia.org/wiki/Server-sent_events) for order book streaming
- The whole order book is updated and rendered on server and sent to client via SSE
  - This is done for simplicity
  - Networking efficiency could be improved by sending order book diffs and merging them on client side
- Uses HTMX for rich UI, this is done for simplicity and the author's reluctance to write javascript
  - HTMX allows to write almost the same complex UI's as frontend frameworks (like react, vue, etc) but much faster and with much lesser code and dependencies
- Order book diff events are persisted in MongoDB
  - Uses [MongoDB watch](https://www.mongodb.com/docs/manual/reference/method/db.collection.watch/) mechanism to consume events and stream them to client

|                 |                                                                                |
| --------------- | ------------------------------------------------------------------------------ |
| `SYMBOL`        | Exchange symbol (default: `BTC/USDT`)                                          |
| `SIMTXT_DB_URI` | Mongo database DSN (default: `mongodb://mongodb:27017/?directConnection=true`) |
| `DB_NAME`       | default `book`                                                                 |
| `ENV`           | default `production`                                                           |
