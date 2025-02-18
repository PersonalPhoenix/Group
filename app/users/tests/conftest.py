import pytest

from httpx import (
    AsyncClient,
    ASGITransport,
)

from app.main import (
    app,
)
from app.config import (
    settings,
)


@pytest.mark.anyio
@pytest.fixture
async def async_animals_client():
    base_url = settings.TEST_URL + settings.DEFAULT_URL_PREFIX_API_V1
    async with AsyncClient(transport=ASGITransport(app=app), base_url=base_url) as async_animals_client:
        yield async_animals_client


@pytest.mark.anyio
@pytest.fixture
async def users_prefix():
    return settings.USERS_PREFIX
