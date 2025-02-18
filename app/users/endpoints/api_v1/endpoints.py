from fastapi import (
    APIRouter,
)


router = APIRouter(
    prefix='/users',
)


@router.get('/get-all')
async def get_all_users():
    pass
