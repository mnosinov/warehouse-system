import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database.database import AsyncSessionLocal, engine
from app.models.user import User
from app.core.security import get_password_hash


async def create_initial_data():
    async with AsyncSessionLocal() as session:
        # Создаем администратора если не существует
        from sqlalchemy import select
        result = await session.execute(select(User).where(User.username == "admin"))
        admin_user = result.scalar_one_or_none()

        if not admin_user:
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            session.add(admin_user)
            await session.commit()
            print("Admin user created: admin / admin123")

        # Создаем тестового оператора
        result = await session.execute(select(User).where(User.username == "operator"))
        operator_user = result.scalar_one_or_none()

        if not operator_user:
            operator_user = User(
                username="operator",
                password_hash=get_password_hash("operator123"),
                role="operator"
            )
            session.add(operator_user)
            await session.commit()
            print("Operator user created: operator / operator123")


if __name__ == "__main__":
    asyncio.run(create_initial_data())