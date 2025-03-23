import json

from fastapi import status
from sqlalchemy.future import select

from backend.users.orm.models import Users
from backend.users.service_layer.helpers import compare_matching_keys
from backend.users.tests.e2e.api_client import (
    delete_user_by_email,
    delete_user_by_id,
    get_all_users,
    get_to_user_by_email,
    get_to_user_by_id,
    get_users_by_filter,
    post_to_create_user,
)
from backend.users.tests.random_refs import generate_test_user_data


async def test_get_users_by_filter(session, async_client_api):
    test_user_data = await generate_test_user_data()
    user = Users(**test_user_data)
    session.add(user)
    await session.commit()

    response = await get_users_by_filter(async_client_api, test_user_data)

    assert response.status_code == status.HTTP_200_OK
    assert await compare_matching_keys(json.loads(response.content).pop(), test_user_data)


async def test_get_all_users(session, async_client_api):
    test_user_data = await generate_test_user_data()
    user = Users(**test_user_data)

    session.add(user)
    await session.commit()

    response = await get_all_users(async_client_api)

    assert response.status_code == status.HTTP_200_OK
    assert await compare_matching_keys(json.loads(response.content).pop(), test_user_data)


async def test_get_user_by_email(session, async_client_api):
    test_user_data = await generate_test_user_data()
    user = Users(**test_user_data)

    session.add(user)
    await session.commit()

    response = await get_to_user_by_email(async_client_api, test_user_data['email'])

    assert response.status_code == status.HTTP_200_OK

    await session.delete(user)
    await session.commit()


async def test_get_user_by_id(session, async_client_api):
    test_user_data = await generate_test_user_data()
    user = Users(**test_user_data)

    session.add(user)
    await session.commit()

    response = await get_to_user_by_id(async_client_api, user.id)

    assert response.status_code == status.HTTP_200_OK

    await session.delete(user)
    await session.commit()


async def test_create_user(session, async_client_api):
    test_user_data = await generate_test_user_data()
    response = await post_to_create_user(async_client_api, test_user_data)

    assert response.status_code == status.HTTP_201_CREATED

    users = await session.execute(select(Users).where(Users.email == test_user_data['email'])) # TODO придумать без SqlAlchemy
    created_user = users.scalar_one()
    user_fields_data = created_user.to_dict()

    assert await compare_matching_keys(user_fields_data, test_user_data)

    await session.delete(created_user)
    await session.commit()


async def test_create_user_if_user_has_been_created(session, async_client_api):
    test_user_data = await generate_test_user_data()
    user = Users(**test_user_data)

    session.add(user)
    await session.commit()

    response = await post_to_create_user(async_client_api, test_user_data)

    await session.delete(user)
    await session.commit()

    assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_delete_user_by_email(session, async_client_api):
    test_user_data = await generate_test_user_data()
    user = Users(**test_user_data)

    session.add(user)
    await session.commit()

    response = await delete_user_by_email(async_client_api, user.email)

    if response.status_code != status.HTTP_200_OK:
        await session.delete(user)
        await session.commit()

    assert response.status_code == status.HTTP_200_OK


async def test_delete_user_by_id(session, async_client_api):
    test_user_data = await generate_test_user_data()
    user = Users(**test_user_data)

    session.add(user)
    await session.commit()

    response = await delete_user_by_id(async_client_api, user.id)

    if response.status_code != status.HTTP_200_OK:
        await session.delete(user)
        await session.commit()

    assert response.status_code == status.HTTP_200_OK
