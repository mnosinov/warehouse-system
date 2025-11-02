# backend/app/admin/admin_setup.py
from sqladmin import Admin
from app.database.database import engine
from .auth_backend import AdminAuth
from .admin_views import UserAdmin, ProductAdmin
from ..core.config import settings


def init_admin(app):
    # Инициализируем бэкенд аутентификации с секретным ключом
    authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
    # Создаем экземпляр Admin
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend, base_url="/admin")
    # Регистрируем созданные View
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    return admin

