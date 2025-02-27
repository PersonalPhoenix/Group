from app.users.domain.commands import (CreateUser, DeleteUserByEmail,
                                       DeleteUserById, GetUserByEmail,
                                       GetUserById)
from app.users.exceptions import NotFoundUser, UserHasAlreadyBeenCreated
from app.users.orm.models import Users
from app.users.service_layer.unit_of_work import AbstractUnitOfWork


async def create_user(
    cmd: CreateUser,
    uow: AbstractUnitOfWork,
):
    async with uow:
        user = await uow.users.get_by_email(email=cmd.email)

        if user is None:
            user = Users(**cmd.__dict__)
            await uow.users.add(user)
        else:
            raise UserHasAlreadyBeenCreated

        await uow.commit()


def get_user_by_email(
    cmd: GetUserByEmail,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get_by_email(email=cmd.email)

        if user is None:
            raise NotFoundUser

    # return user.get_info()


def get_user_by_id(
    cmd: GetUserById,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get_by_id(id=cmd.id)

        if user is None:
            raise NotFoundUser

    # return user.get_info()


def delete_user_by_email(
    cmd: DeleteUserByEmail,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get_by_email(email=cmd.email)

        if user is None:
            raise NotFoundUser

        uow.users.delete_by_email(user.email)

        uow.commit()


def delete_user_by_id(
    cmd: DeleteUserById,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get_by_id(id=cmd.id)

        if user is None:
            raise NotFoundUser

        uow.users.delete_by_id(user)

        uow.commit()


COMMAND_HANDLERS = {
    CreateUser: create_user,
    GetUserById: get_user_by_id,
    GetUserByEmail: get_user_by_email,
    DeleteUserById: delete_user_by_id,
    DeleteUserByEmail: delete_user_by_email,
}
