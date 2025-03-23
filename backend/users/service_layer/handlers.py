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
from backend.users.orm.models import Users
from backend.users.service_layer.unit_of_work import AbstractUnitOfWork


async def create_user(
    cmd: CreateUser,
    uow: AbstractUnitOfWork,
):
    """Создаёт пользователя.

    Raises:
        UserHasAlreadyBeenCreated: пользователь не найден.
    """

    async with uow:
        user = await uow.users.get_by_email(email=cmd.email) or await uow.users.get_by_tag(tag=cmd.tag)

        if user is None:
            user = Users(**cmd.__dict__)
            await uow.users.add(user)
        else:
            raise UserHasAlreadyBeenCreated


async def get_all_users(
    cmd: GetAllUsers,
    uow: AbstractUnitOfWork,
):
    """Возвращает всех пользователь."""

    async with uow:
        users = await uow.users.get_all()
        users_data = [user.to_dict() for user in users]

    return users_data


async def get_user_by_email(
    cmd: GetUserByEmail,
    uow: AbstractUnitOfWork,
):
    """Находит данные пользователя по почте."""

    async with uow:
        user = await uow.users.get_by_email(email=cmd.email)

        if user is None:
            raise NotFoundUser
        else:
            user_data = user.to_dict

    return user_data


async def get_user_by_tag(
    cmd: GetUserByEmail,
    uow: AbstractUnitOfWork,
):
    """Находит данные пользователя по тегу."""

    async with uow:
        user = await uow.users.get_by_tag(email=cmd.tag)

        if user is None:
            raise NotFoundUser
        else:
            user_data = user.to_dict

    return user_data


async def get_user_by_id(
    cmd: GetUserById,
    uow: AbstractUnitOfWork,
):
    """Находит данные пользователя по идентификатору."""

    async with uow:
        user = await uow.users.get_by_id(id=cmd.id)

        if user is None:
            raise NotFoundUser
        else:
            user_data = user.to_dict()

        return user_data


async def get_users_by_filter(
    cmd: GetUsersByFilter,
    uow: AbstractUnitOfWork,
):
    """Находит пользотелей соответствующим указанным фильтрам."""

    async with uow:
        user_filter_params = cmd.get_is_not_none_attribute()
        users = await uow.users.get_by_filter(user_filter_params)
        users_data = [user.to_dict() for user in users]

        return users_data


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


COMMAND_HANDLERS = {
    CreateUser: create_user,
    GetAllUsers: get_all_users,
    GetUsersByFilter: get_users_by_filter,
    GetUserById: get_user_by_id,
    GetUserByEmail: get_user_by_email,
    DeleteUserById: delete_user_by_id,
    DeleteUserByEmail: delete_user_by_email,
}
