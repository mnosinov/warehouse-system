from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from sqlalchemy import select
from app.database.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import verify_password

class AdminAuth(AuthenticationBackend):

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Используем асинхронную сессию для проверки пользователя
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()

        # Проверяем существование пользователя, пароль и роль
        if user and verify_password(password, user.password_hash) and user.role == "admin":
            # Обновляем сессию, добавляя в нее токен
            request.session.update({"token": user.username})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Очищаем сессию при выходе
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        # Проверяем, аутентифицирован ли пользователь
        token = request.session.get("token")
        return token is not None