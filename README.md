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
  - HTMX allows to write UIs of almost the same complexity as frontend frameworks (like react, vue, etc) but much faster and with much lesser code and dependencies
- Order book diff events are persisted in MongoDB
  - Uses [MongoDB watch](https://www.mongodb.com/docs/manual/reference/method/db.collection.watch/) mechanism to consume events and stream them to client

## Running

To run production build do the following. This will fetch pre-built images from docker hub and run docker-compose.

```
make run
```

You can also specify symbol for order book:

```
make run SYMBOL=ETH/USDT
```

### App Environment Variables

| Env Var     | Description                                                             |
| ----------- | ----------------------------------------------------------------------- |
| `SYMBOL`    | Exchange symbol (default: `BTC/USDT`)                                   |
| `MONGO_DSN` | MongoDB DSN (default: `mongodb://mongodb:27017/?directConnection=true`) |
| `DB_NAME`   | default `book`                                                          |
| `ENV`       | default `production`                                                    |

## Development

```
poetry install
make dev # run in another terminal, this will start mongodb via docker-compose
python book/worker.py # run in another terminal, starts worker that consumes binance order book diff events and stores them in DB
ENV=development uvicorn book.app:app --reload-include '*.html' --reload
```
