from fastapi import status, HTTPException


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")


class TokenNoFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден")


UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует")

PasswordMismatchException = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пароли не совпадают!")

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
)

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не валидный!")

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Не найден ID пользователя")

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав!")


"""
В этом фрагменте кода мы определили несколько пользовательских исключений для обработки различных 
ошибок, связанных с аутентификацией и авторизацией в FastAPI. Вот краткое описание:

TokenExpiredException: Исключение, вызываемое при истечении срока действия токена (HTTP 401).

TokenNoFoundException: Исключение, вызываемое при отсутствии токена (HTTP 401).

UserAlreadyExistsException: Исключение, вызываемое при попытке создать пользователя, 
который уже существует (HTTP 409).

PasswordMismatchException: Исключение, вызываемое при несовпадении паролей (HTTP 409).

IncorrectEmailOrPasswordException: Исключение, вызываемое при неверной почте или пароле (HTTP 401).

NoJwtException: Исключение, вызываемое при отсутствии или недействительности токена (HTTP 401).

NoUserIdException: Исключение, вызываемое при отсутствии ID пользователя (HTTP 401).

ForbiddenException: Исключение, вызываемое при недостатке прав доступа (HTTP 403).
"""
