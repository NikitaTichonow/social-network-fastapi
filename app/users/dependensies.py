from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from config import get_auth_data
from exceptions import TokenExpiredException, NoJwtException, NoUserIdException, TokenNoFoundException
from users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data["secret_key"], algorithms=auth_data["algorithm"])
    except JWTError:
        raise NoJwtException

    expire: str = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get("sub")
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


"""
Функция get_token: Извлекает токен из cookies запроса. Если токен отсутствует, 
выбрасывается исключение TokenNoFoundException.

Функция get_current_user:

Декодирует токен с использованием секретного ключа и алгоритма из конфигурации.

Проверяет срок действия токена. Если токен истек, выбрасывается исключение 
TokenExpiredException.

Извлекает ID пользователя из токена. Если ID отсутствует, выбрасывается 
исключение NoUserIdException.

Ищет пользователя в базе данных по ID. Если пользователь не найден, выбрасывается 
исключение HTTPException с кодом 401.

Возвращает найденного пользователя.

Этот код обеспечивает безопасную аутентификацию пользователей
"""
