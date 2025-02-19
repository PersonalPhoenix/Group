from app.users.domain.commands import (
    CreateUser,
    DeleteUserByEmail,
    DeleteUserById,
    GetUserByEmail,
    GetUserById,
)
from app.users.domain.models import User
from app.users.exceptions import NotFoundUser, UserAlreadyBeenCreated
from app.users.service_layer.unit_of_work import AbstractUnitOfWork


def create_user(
    cmd: CreateUser,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(email=cmd.email)
        
        if user is None:
            user = User(cmd.email, cmd.password)
            uow.users.add(user)
        else:
            raise UserAlreadyBeenCreated

        uow.commit()


def get_user_by_email(
    cmd: GetUserByEmail,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(email=cmd.email)
        
        if user is None:
            raise NotFoundUser
        
        user = User(email=user.email)

    return user.get_info()


def get_user_by_id(
    cmd: GetUserById,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(id=cmd.id)
        
        if user is None:
            raise NotFoundUser
        
        user = User(id=user.id)

    return user.get_info()


def delete_user_by_email(
    cmd: DeleteUserByEmail,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(email=cmd.email)

        if user is None:
            raise NotFoundUser

        uow.users.delete_by_email(user.email)

        uow.commit()


def delete_user_by_id(
    cmd: DeleteUserById,
    uow: AbstractUnitOfWork,
):
    with uow:
        user = uow.users.get(id=cmd.id)
        
        if user is None:
            raise NotFoundUser
        
        uow.users.delete_by_id(user)
        
        uow.commit()


COMMAND_HADLERS = {
    CreateUser: create_user,
    GetUserById: get_user_by_id,
    GetUserByEmail: get_user_by_email,
    DeleteUserById: delete_user_by_id,
    DeleteUserByEmail: delete_user_by_email,
}