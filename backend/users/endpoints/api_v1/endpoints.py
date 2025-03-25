
from fastapi import APIRouter, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from fastapi import Response
from backend.bootstrap import bootstrap
from backend.config import settings
from backend.users.domain.commands import (
    RegisterUser,
    DeleteUserByEmail,
    DeleteUserById,
)
from backend.users.domain.queries import (
    GetAllUsers,
    GetUserByEmail,
    GetUserById,
    GetUsersByFilter,
    AuthenticateUser, GetCurrentUser,
)
from backend.users.exceptions import NotFoundUser, UserHasAlreadyBeenCreated, TokenIsInvalid, TokenExpired, \
    TokenNotHaveUserId, IncorrectInfoForAuthenticateUser
from backend.users.service_layer.auth import create_access_token

router = APIRouter(
    tags=[settings.USERS_TAG],
    prefix=settings.USERS_PREFIX,
)

bus = bootstrap()


@router.get('/get_all')
async def get_all_users():
    """Возвращает данные всех пользователей в системе."""

    query = GetAllUsers()
    users_data = await bus.handle(query)

    return JSONResponse(content=jsonable_encoder(users_data))


@router.get('/get_by_filter/')
async def get_user_by_filter(
    id: int = None,
    email: EmailStr = None,
    tag: str = None,
    role_id: int = None,
):
    """Возвращает данные пользователей подходящих по фильтру."""

    query = GetUsersByFilter(id, tag, email, role_id)
    users_data = await bus.handle(query)

    return JSONResponse(content=jsonable_encoder(users_data))


@router.get('/get_by_email/{email}')
async def get_user_by_email(email: EmailStr):
    """Возвращает данные пользователя, найденного по почте.

    Raises:
        HTTPException(404): не удалось найти нужного пользователя по указанной почте.
    """

    try:
        query = GetUserByEmail(email=email)
        user_data = await bus.handle(query)
    except NotFoundUser:
        raise HTTPException(status_code=404, detail=f'Failed: Not found user with email {query.email}')

    return JSONResponse(content=jsonable_encoder(user_data))


@router.get('/get_by_id/{id}')
async def get_user_by_id(id: int):
    """Возвращает данные пользователя, найденного по идентификатору.

    Raises:
        HTTPException(404): не удалось найти нужного пользователя по указанному идентификатору.
    """

    try:
        query = GetUserById(id=id)
        user_data = await bus.handle(query)
    except NotFoundUser:
        raise HTTPException(status_code=404, detail=f'Failed: Not found user with id {query.id}')

    return JSONResponse(content=jsonable_encoder(user_data))


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(cmd: RegisterUser):
    """Создаёт пользователя по данным переданным в теле запроса.

    Raises:
        HTTPException(400): Пользователь с такой почтой уже зарегистрирован.
    """

    try:
        await bus.handle(cmd)
    except UserHasAlreadyBeenCreated:
        raise HTTPException(status_code=400, detail=f'Failed: User has already been created with email {cmd.email}')
    else:
        return f'Success: User create with email {cmd.email}'


@router.post("/login/")
async def auth_user(response: Response, query: AuthenticateUser):
    try:
        user_id = await bus.handle(query)
    except IncorrectInfoForAuthenticateUser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')

    access_token = create_access_token({"sub": str(user_id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)

    return {'access_token': access_token, 'refresh_token': None}


@router.post("/logout/", status_code=status.HTTP_200_OK)
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")

    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me/")
async def get_me(request: Request):
    token = request.cookies.get('users_access_token')

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')

    query = GetCurrentUser(token=token)

    try:
        user_data = await bus.handle(query)
    except TokenIsInvalid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')
    except TokenExpired:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')
    except TokenNotHaveUserId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    except NotFoundUser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Пользователь не найден')

    return user_data


@router.delete('/delete_by_id/{id}')
async def delete_user_by_id(id: int):
    """Удаляет пользователя, найденного по идентификатору.

    Raises:
        HTTPException(404): Пользователь с таким идентификатором не был найден.
    """

    try:
        cmd = DeleteUserById(id=id)
        await bus.handle(cmd)
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
        await bus.handle(cmd)
    except NotFoundUser:
        raise HTTPException(status_code=404, detail=f'Failed: Not found user with email {cmd.email}')
    else:
        return f'Success: User delete with email {cmd.email}'
