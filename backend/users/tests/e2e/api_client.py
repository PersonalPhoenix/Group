from typing import Any

from httpx import AsyncClient
from pydantic import EmailStr

from backend.users.domain.commands import GetUsersByFilter


async def post_to_create_user(client: AsyncClient, user_data: EmailStr):
    response = await client.post(
        '/users/create',
        json={
            **user_data,
        },
    )

    return response


async def get_users_by_filter(client: AsyncClient, params: dict[str, Any]):
    request_params = '&'.join([
        f'{key}={value}'
        for key, value in params.items()
        if key in GetUsersByFilter.__annotations__
    ])

    response = await client.get(
        f'users/get_by_filter/?{request_params}'
    )

    return response


async def get_all_users(client: AsyncClient):
    response = await client.get(
        'users/get_all',
    )

    return response


async def get_to_user_by_email(client: AsyncClient, user_email: EmailStr):
    response = await client.get(
        f'users/get_by_email/{user_email}',
    )

    return response


async def get_to_user_by_id(client: AsyncClient, user_id: int):
    response = await client.get(
        f'users/get_by_id/{user_id}',
    )

    return response


async def delete_user_by_id(client: AsyncClient, user_id: int):
    response = await client.delete(
        f'users/delete_by_id/{user_id}',
    )

    return response


async def delete_user_by_email(client: AsyncClient, user_email: EmailStr):
    response = await client.delete(
        f'users/delete_by_email/{user_email}',
    )

    return response
