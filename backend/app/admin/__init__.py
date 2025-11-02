from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from app.core.security import verify_token
from app.database.database import engine
from app.models import User, Product


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        # Здесь должна быть проверка учетных данных администратора
        # Пока используем простую проверку для демо
        if username == "admin" and password == "admin":
            request.session.update({"token": "admin-token"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.role, User.is_active, User.created_at]
    can_delete = False
    form_excluded_columns = [User.password_hash]


class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.sku, Product.current_quantity, Product.min_quantity,
                   Product.max_quantity]
    form_columns = [Product.name, Product.description, Product.sku, Product.current_quantity, Product.min_quantity,
                    Product.max_quantity]

# Инициализация будет в main.py