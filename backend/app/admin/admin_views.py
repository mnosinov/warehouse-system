from sqladmin import ModelView
from starlette.requests import Request
from app.models.user import User
from app.models.product import Product

class UserAdmin(ModelView, model=User):
    # Колонки, отображаемые в списке
    column_list = [User.id, User.username, User.role, User.is_active]
    # Колонки, по которым можно вести поиск
    column_searchable_list = [User.username]
    # Поля, исключенные из формы создания/редактирования
    form_excluded_columns = [User.password_hash]

    # Ограничение доступа: только админы
    def is_accessible(self, request: Request) -> bool:
        # Здесь должна быть ваша логика проверки роли, например, через запрос к БД по username из request.session
        # Для примера используется упрощенная проверка
        return True

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.sku, Product.current_quantity, Product.min_quantity, Product.max_quantity]
    column_searchable_list = [Product.name, Product.sku]
    column_sortable_list = [Product.id, Product.name, Product.current_quantity]

    def is_accessible(self, request: Request) -> bool:
        return True