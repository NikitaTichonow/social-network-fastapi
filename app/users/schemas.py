from pydantic import BaseModel, EmailStr, Field


class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    password_check: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")


"""
Первая модель (SUserRegister) будет использоваться при регистрации пользователей. 
В этой модели прописан email, password, password_check и name – те поля, которые 
будет заполнять пользователь при регистрации.

Вторая модель (SUserAuth) будет использоваться при авторизации пользователя. 
Тут он будет отправлять свой  email и пароль.
"""
