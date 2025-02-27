import pytest

from httpx import (
    ASGITransport,
    AsyncClient,
)

from app.config import (
    settings,
)
from app.main import (
    app,
)


@pytest.mark.anyio
@pytest.fixture
async def async_client_api_v1():
    base_url = settings.TEST_URL + settings.DEFAULT_URL_PREFIX_API_V1
    transport = ASGITransport(
        app=app,
    )
    client = AsyncClient(
        transport=transport, 
        base_url=base_url,
    )

    async with client as async_animals_client:
        yield async_animals_client
