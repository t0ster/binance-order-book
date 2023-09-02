from httpx import AsyncClient
from pytest_mock import MockerFixture


async def test_index(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200


async def test_stream(client: AsyncClient, mocker: MockerFixture):
    # TODO
    mocker.patch("book.routes.get_order_book_snapshot")
    mocker.patch("book.routes.stream_order_book")
    response = await client.get("/stream")
    assert response.status_code == 200
