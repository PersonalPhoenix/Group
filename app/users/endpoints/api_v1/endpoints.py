from fastapi import (
    APIRouter,
)

from app.config import (
    settings,
)


router = APIRouter(
    tags=[settings.USERS_TAG],
    prefix=settings.USERS_PREFIX,
)


@router.get('/get-all')
async def get_all_users():
    pass
