from uuid import uuid4


async def random_suffix():
    return uuid4().hex

async def random_email():
    return f'{await random_suffix()}@mail.ru'

async def random_tag():
    return f'@{await random_suffix()}'

async def generate_test_user_data():
    return {
        'email': await random_email(),
        'password': 'string',
        'tag': await random_tag(),
        'role_id': 1,
    }
