# backend/app/admin/__init__.py
from .admin_views import UserAdmin, ProductAdmin
from .auth_backend import AdminAuth

# Опционально: можно импортировать функцию для удобства
from .admin_setup import init_admin

__all__ = ["AdminAuth", "UserAdmin", "ProductAdmin", "init_admin"]

# Инициализация будет в main.py