
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import EmailStr

from backend.config import settings
from backend.users.domain.commands import (
    CreateUser,
    DeleteUserByEmail,
    DeleteUserById,
    GetAllUsers,
    GetUserByEmail,
    GetUserById,
    GetUsersByFilter,
)
from backend.users.exceptions import NotFoundUser, UserHasAlreadyBeenCreated
from backend.users.service_layer.handlers import COMMAND_HANDLERS
from backend.users.service_layer.unit_of_work import UserSqlAlchemyUnitOfWork

router = APIRouter(
    tags=[settings.USERS_TAG],
    prefix=settings.USERS_PREFIX,
)


@router.get('/get_all')
async def get_all_users():
    """Возвращает данные всех пользователей в системе."""

    cmd = GetAllUsers()
    command_handler = COMMAND_HANDLERS[type(cmd)]
    users_data = await command_handler(cmd, UserSqlAlchemyUnitOfWork())

    return JSONResponse(content=jsonable_encoder(users_data))


@router.get('/get_by_filter/')
async def get_user_by_filter(id: int = None, email: EmailStr = None, tag: str = None, role_id: int = None):
    """Возвращает данные пользователей подходящих по фильтру."""

    cmd = GetUsersByFilter(id, tag, email, role_id)
    command_handler = COMMAND_HANDLERS[type(cmd)]
    users_data = await command_handler(cmd, UserSqlAlchemyUnitOfWork())

    return JSONResponse(content=jsonable_encoder(users_data))


@router.get('/get_by_email/{email}')
async def get_user_by_email(email: EmailStr):
    """Возвращает данные пользователя, найденного по почте.

    Raises:
        HTTPException(404): не удалось найти нужного пользователя по указанной почте.
    """

    try:
        cmd = GetUserByEmail(email=email)
        command_handler = COMMAND_HANDLERS[type(cmd)]
        user_data = await command_handler(cmd, UserSqlAlchemyUnitOfWork())
    except NotFoundUser:
        raise HTTPException(status_code=404, detail=f'Failed: Not found user with email {cmd.email}')

    return JSONResponse(content=jsonable_encoder(user_data))


@router.get('/get_by_id/{id}')
async def get_user_by_id(id: int):
    """Возвращает данные пользователя, найденного по идентификатору.

    Raises:
        HTTPException(404): не удалось найти нужного пользователя по указанному идентификатору.
    """

    try:
        cmd = GetUserById(id=id)
        command_handler = COMMAND_HANDLERS[type(cmd)]
        user_data = await command_handler(cmd, UserSqlAlchemyUnitOfWork())
    except NotFoundUser:
        raise HTTPException(status_code=404, detail=f'Failed: Not found user with id {cmd.id}')

    return JSONResponse(content=jsonable_encoder(user_data))



@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(cmd: CreateUser):
    """Создаёт пользователя по данным переданным в теле запроса.

    Raises:
        HTTPException(400): Пользователь с такой почтой уже зарегистрирован.
    """

    try:
        command_handler = COMMAND_HANDLERS[type(cmd)]
        await command_handler(cmd, UserSqlAlchemyUnitOfWork())
    except UserHasAlreadyBeenCreated:
        raise HTTPException(status_code=400, detail=f'Failed: User has already been created with email {cmd.email}')
    else:
        return f'Success: User create with email {cmd.email}'


@router.delete('/delete_by_id/{id}')
async def delete_user_by_id(id: int):
    """Удаляет пользователя, найденного по идентификатору.

    Raises:
        HTTPException(404): Пользователь с таким идентификатором не был найден.
    """

    try:
        cmd = DeleteUserById(id=id)
        command_handler = COMMAND_HANDLERS[type(cmd)]
        await command_handler(cmd, UserSqlAlchemyUnitOfWork())
    except NotFoundUser:
        raise HTTPException(status_code=404, detail=f'Failed: Not found user with id {cmd.id}')
    else:
        return f'Success: User delete with id {cmd.id}'


@router.delete('/delete_by_email/{email}')
async def delete_user_by_email(email: EmailStr):
    """Удаляет пользователя, найденного по почте.

    Raises:
        HTTPException(404): Пользователь с такой почтой не был найден.
    """

    try:
        cmd = DeleteUserByEmail(email=email)
        command_handler = COMMAND_HANDLERS[type(cmd)]
        await command_handler(cmd, UserSqlAlchemyUnitOfWork())
    except NotFoundUser:
        raise HTTPException(status_code=404, detail=f'Failed: Not found user with email {cmd.email}')
    else:
        return f'Success: User delete with email {cmd.email}'
