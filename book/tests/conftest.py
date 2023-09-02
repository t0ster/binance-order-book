import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from book.app import app
from book.config import settings


@pytest.fixture(scope="session", autouse=True)
def config_tests(session_mocker: MockerFixture):
    session_mocker.patch.object(settings, "DB_NAME", settings.DB_NAME + "_test")
    yield
    # TODO: teardown


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
