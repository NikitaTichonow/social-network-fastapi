from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, PasswordMismatchException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister, SUserAuth

router = APIRouter(prefix="/auth", tags=["Auth"])


"""
Этот код реализует базовые функции регистрации, авторизации и выхода пользователя в веб-приложении на FastAPI. 
"""


@router.post("/register/")  # Регистрация пользователя
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(
        email=user_data.email
    )  # Проверка, существует ли пользователь с данным email.
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:  # Проверка совпадения паролей.
        raise PasswordMismatchException("Пароли не совпадают")
    hashed_password = get_password_hash(
        user_data.password
    )  # Хеширование пароля и добавление нового пользователя в базу данных.
    await UsersDAO.add(name=user_data.name, email=user_data.email, hashed_password=hashed_password)

    return {"message": "Вы успешно зарегистрированы!"}  # Возвращение сообщения об успешной регистрации.


@router.post("/login/")  # Авторизация пользователя
async def auth_user(response: Response, user_data: SUserAuth):  # Аутентификация пользователя по email и паролю.
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})  # Создание и установка токена доступа в cookie.
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        "ok": True,
        "access_token": access_token,
        "refresh_token": None,
        "message": "Авторизация успешна!",
    }  # Возвращение сообщения об успешной авторизации.


@router.post("/logout/")  # Выход пользователя
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")  # Удаление cookie с токеном доступа.
    return {"message": "Пользователь успешно вышел из системы"}  # Возвращение сообщения об успешном выходе.
