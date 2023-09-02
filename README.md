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
- Uses HTMX on frontend
  - HTMX is a simple and elegant solution that allows to write UIs of almost the same complexity as frontend frameworks (like react, vue, etc) but much faster and with much lesser code and dependencies
- Order book diff events are persisted in MongoDB
  - This could be used to "replay" order book or build a heatmap (not implemented)
  - Uses [MongoDB watch](https://www.mongodb.com/docs/manual/reference/method/db.collection.watch/) mechanism to consume events and stream them to client
    - This could be useful to prevent hitting API rate limits, however may increase latency a little bit
    - Another option could be to open a web socket connection to Binance for each user on the backend
    - One more option with the least latency could be to open a ws connection to Binance in browser

- If tests pass docker image is built automatically by GithHub action and uploaded to Docker Hub

## Running

To run production build do the following. This will fetch pre-built images from docker hub and run docker-compose.

```
make run
```

Open http://localhost:8000

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

`?directConnection=true` is required for local mongo deployment because it is deployed as single node replica set, which is required to enable oplog (for watch functionality)

## Development

```
poetry install
make dev # run in another terminal, this will start mongodb via docker-compose
poetry shell # activates virtualenv
python book/worker.py # run in another terminal, starts worker that consumes binance order book diff events and stores them in DB
ENV=development uvicorn book.app:app --reload-include '*.html' --reload
```

To run tests:

```
pytests
```
