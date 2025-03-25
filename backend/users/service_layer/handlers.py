from datetime import datetime, timezone
from http.client import HTTPException
from typing import Type, Dict, Callable, List

from authlib.jose import jwt
from jose import JWTError
from starlette import status

from backend.config import settings
from backend.core.adapters.notifications import AbstractNotifications
from backend.core.service_layer.unit_of_work import AbstractUnitOfWork
from backend.users.domain.commands import (
    RegisterUser,
    DeleteUserByEmail,
    DeleteUserById,
    Command,
)
from backend.users.domain.queries import (
    GetAllUsers,
    GetUserByEmail,
    GetUserById,
    GetUsersByFilter,
    Query,
    GetUserByTag,
    AuthenticateUser, GetCurrentUser,
)
from backend.users.domain.events import CreatedUser, Event
from backend.users.exceptions import NotFoundUser, UserHasAlreadyBeenCreated, TokenIsInvalid, TokenExpired, \
    TokenNotHaveUserId, IncorrectInfoForAuthenticateUser
from backend.users.orm.models import Users
from backend.users.service_layer.auth import get_password_hash, verify_password


async def register_user(
    cmd: RegisterUser,
    uow: AbstractUnitOfWork,
):
    """Создаёт пользователя.

    Raises:
        UserHasAlreadyBeenCreated: пользователь не найден.
    """

    async with uow:
        user = await uow.users.get_by_email(email=cmd.email) or await uow.users.get_by_tag(tag=cmd.tag)

        if user is None:
            cmd.password = get_password_hash(cmd.password)
            user = Users(**cmd.__dict__)
            await uow.users.add(user)
        else:
            raise UserHasAlreadyBeenCreated


async def authenticate_user(
    cmd: AuthenticateUser,
    uow: AbstractUnitOfWork,
):
    """Создаёт пользователя.

    Raises:
        UserHasAlreadyBeenCreated: пользователь не найден.
    """

    async with uow:
        user = await uow.users.get_by_email(email=cmd.email)

        if user is None or verify_password(plain_password=cmd.password, hashed_password=user.password) is False:
            raise IncorrectInfoForAuthenticateUser

        user_id = user.to_dict()['id']

    return user_id


async def get_all_users(
    query: GetAllUsers,
    uow: AbstractUnitOfWork,
):
    """Возвращает всех пользователь."""

    async with uow:
        users = await uow.users.get_all()
        users_data = [user.to_dict() for user in users]

    return users_data


async def get_user_by_email(
    query: GetUserByEmail,
    uow: AbstractUnitOfWork,
):
    """Находит данные пользователя по почте."""

    async with uow:
        user = await uow.users.get_by_email(email=query.email)

        if user is None:
            raise NotFoundUser
        else:
            user_data = user.to_dict

    return user_data


async def get_user_by_tag(
    query: GetUserByTag,
    uow: AbstractUnitOfWork,
):
    """Находит данные пользователя по тегу."""

    async with uow:
        user = await uow.users.get_by_tag(email=query.tag)

        if user is None:
            raise NotFoundUser
        else:
            user_data = user.to_dict

    return user_data


async def get_user_by_id(
    query: GetUserById,
    uow: AbstractUnitOfWork,
):
    """Находит данные пользователя по идентификатору."""

    async with uow:
        user = await uow.users.get_by_id(id=query.id)

        if user is None:
            raise NotFoundUser
        else:
            user_data = user.to_dict()

        return user_data


async def get_users_by_filter(
    query: GetUsersByFilter,
    uow: AbstractUnitOfWork,
):
    """Находит пользотелей соответствующим указанным фильтрам."""

    async with uow:
        user_filter_params = query.get_is_not_none_attribute()
        users = await uow.users.get_by_filter(user_filter_params)
        users_data = [user.to_dict() for user in users]

        return users_data


async def get_current_user(
    query: GetCurrentUser,
    uow: AbstractUnitOfWork,
):
    try:
        auth_data = settings.get_auth_data
        # payload = jwt.decode(query.token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
        payload = jwt.decode(query.token[2:-1], auth_data['secret_key'])
    except JWTError:
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
        raise TokenIsInvalid

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
        raise TokenExpired

    user_id = payload.get('sub')
    if not user_id:
        raise TokenNotHaveUserId

    async with uow:
        user = await uow.users.get_by_id(id=int(user_id))

        if not user:
            raise NotFoundUser

        user_data = user.to_dict()

    return user_data


async def delete_user_by_email(
    cmd: DeleteUserByEmail,
    uow: AbstractUnitOfWork,
):
    """Удаляет пользователя по почте."""

    async with uow:
        user = await uow.users.get_by_email(email=cmd.email)

        if user is None:
            raise NotFoundUser
        else:
            delete_user = await uow.users.delete(user)

    return delete_user


async def delete_user_by_id(
    cmd: DeleteUserById,
    uow: AbstractUnitOfWork,
):
    """Удаляет пользователя по идентификатору."""

    async with uow:
        user = await uow.users.get_by_id(id=cmd.id)

        if user is None:
            raise NotFoundUser
        else:
            delete_user = await uow.users.delete(user)

    return delete_user


async def send_notification_about_created_user(
    event: CreatedUser,
    notifications: AbstractNotifications,
):
    await notifications.send(
        event.email,
        'Пользователь успешно создан',
    )


COMMAND_HANDLERS: Dict[Type[Command], Callable] = {
    RegisterUser: register_user,

    DeleteUserById: delete_user_by_id,
    DeleteUserByEmail: delete_user_by_email,
}

EVENT_HANDLERS: Dict[Type[Event], List[Callable]] = {
    CreatedUser: [send_notification_about_created_user],
}

QUERY_HANDLERS: Dict[Type[Query], Callable] = {
    AuthenticateUser: authenticate_user,
    GetCurrentUser: get_current_user,
    GetAllUsers: get_all_users,
    GetUsersByFilter: get_users_by_filter,
    GetUserById: get_user_by_id,
    GetUserByEmail: get_user_by_email,
}
