from fastapi import (
    APIRouter,
)

from app.config import (
    settings,
)
from app.users.endpoints.api_v1.endpoints import (
    router as users_router,
)


router = APIRouter(
    tags=[settings.DEFAULT_TAG_V1],
    prefix=settings.DEFAULT_URL_PREFIX_V1
)


router.include_router(
    router=users_router,
)
