from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta, timezone
from config import get_auth_data
from app.users.dao import UsersDAO


# Функция create_access_token: создает JWT‑токен с заданными данными и сроком действия
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=366)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encode_jwt = jwt.encode(to_encode, auth_data["secret_key"], algorithm=auth_data["algorithm"])
    return encode_jwt


# Контекст хэширования паролей: Настраивается контекст для хэширования паролей с использованием алгоритма bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция get_password_hash: Хэширует пароль.
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Функция verify_password: Проверяет соответствие введенного пароля и хэшированного пароля.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Функция authenticate_user: Проверяет наличие пользователя и корректность его пароля.
async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.hashed_password) is False:
        return None
    return user
