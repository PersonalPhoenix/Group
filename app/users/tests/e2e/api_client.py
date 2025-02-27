import requests
from config import settings


def post_to_create_user(email, password, tag, role_id=1):
    url = settings.get_api_url
    response = requests.post(
        f'{url}/users/create',
        json={
            'email': email,
            'password': password,
            'tag': tag,
            'role_id': role_id,
        },
    )

    assert response == 201

