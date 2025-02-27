from fastapi import APIRouter

from app.config import settings
from app.users.domain.commands import CreateUser
from app.users.exceptions import UserHasAlreadyBeenCreated
from app.users.service_layer.handlers import COMMAND_HANDLERS
from app.users.service_layer.unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter(
    tags=[settings.USERS_TAG],
    prefix=settings.USERS_PREFIX,
)


@router.get('/get-all')
async def get_all_users():
    pass


@router.get('/get_by_email')
async def get_user_by_email():
    pass


@router.get('/get_by_id')
async def get_user_by_id():
    pass


@router.post('/create')
async def create_user(cmd: CreateUser):
    try:
        command_handler = COMMAND_HANDLERS[cmd.__class__]
        await command_handler(cmd, SqlAlchemyUnitOfWork())
    except UserHasAlreadyBeenCreated:
        return f'Failed: User has already been created with email {cmd.email}', 400
    else:
        return f'Success: User create with email {cmd.email}', 201


@router.delete('/delete_by_id')
async def delete_user_by_id():
    pass


@router.delete('/delete_by_email')
async def delete_user_by_email():
    pass
