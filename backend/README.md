# Основные моменты
- Асинхронные запросы с asyncpg
- JWT аутентификация с ролями
- SQLAdmin панель
- Pydantic схемы для валидации
- CORS настроен через .env
- HTTPS с самоподписанными сертификатами
- Ролевая модель (admin/operator)
- Хэширование паролей

# Бэкенд (FastAPI + PostgreSQL)
```text
backend/
├── app/
│   ├── models/          # SQLAlchemy модели
│   ├── schemas/         # Pydantic схемы
│   ├── api/             # FastAPI роутеры
│   ├── core/            # Настройки, JWT, security
│   ├── database/        # Настройка DB
│   └── admin/           # SQLAdmin панель
```



# БАЗА ДАННЫХ
## Типичный workflow работы с миграциями:
```bash
# 1. Создание новой миграции (после изменения моделей)
alembic revision --autogenerate -m "Описание изменений"

# 2. Применение миграций
alembic upgrade head

# 3. Откат миграции (если что-то пошло не так)
alembic downgrade -1

# 4. Просмотр истории миграций
alembic history

# 5. Проверка текущей версии
alembic current
```

## Конкретные сценарии использования в нашем проекте:
### 1. Добавление новых таблиц
```python
# Когда добавляем новую модель, например для истории движений:
# backend/app/models/stock_movement.py

class StockMovement(Base):
    __tablename__ = "stock_movements"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    movement_type = Column(String(20))  # 'incoming', 'outgoing', 'adjustment'
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```
Создаем миграцию:

```bash
alembic revision --autogenerate -m "Add stock_movements table"
```
### 2. Изменение существующих таблиц
```python
# Добавляем новое поле в существующую модель
# backend/app/models/product.py

class Product(Base):
    # существующие поля...
    category = Column(String(50), nullable=True)  # новое поле
```
Создаем миграцию:

```bash
alembic revision --autogenerate -m "Add category to products"
```
### 3. Миграции данных
```python
# Иногда нужно не только изменить схему, но и данные
# alembicmigrations/versions/002_add_default_categories.py

def upgrade():
    # Добавляем колонку
    op.add_column('products', sa.Column('category', sa.String(50), nullable=True))
    
    # Миграция данных
    connection = op.get_bind()
    connection.execute(
        "UPDATE products SET category = 'electronics' WHERE category IS NULL"
    )

def downgrade():
    op.drop_column('products', 'category')
```
### 4. Работа в команде
```bash
# Когда коллега добавил новую миграцию
git pull
alembic upgrade head

# После внесения изменений в модели
alembic revision --autogenerate -m "Your changes"
git add alembicmigrations/versions/
git commit -m "Add database migration"
```
### 5. Production deployment
```bash
# В CI/CD пайплайне или при деплое
alembic upgrade head

# С откатом при ошибке
alembic upgrade head || alembic downgrade -1
```
## Best Practices для проекта:
### 1. Структура миграций:
```
alembic/
├── versions/
│   ├── 001_initial.py
│   ├── 002_add_stock_movements.py
│   ├── 003_add_inventory_checks.py
│   └── 004_add_indexes.py
```
### 2. Правила именования:
```bash
# Хорошо
alembic revision --autogenerate -m "add_user_email_index"

# Плохо
alembic revision --autogenerate -m "update"
```
### 3. Проверка миграций:
```bash
# Всегда проверяйте сгенерированную миграцию
cat alembicmigrations/versions/xxx_add_new_table.py

# Тестируйте откат
alembic downgrade -1
alembic upgrade head
```

## Важно!:
1. Никогда не редактируйте примененные миграции - создавайте новые
2. Всегда бэкапьте базу перед миграциями в production
3. Тестируйте миграции на staging окружении
4. Используйте --autogenerate осторожно - проверяйте сгенерированный код

### Workflow для работы в команде:
- Изменяете модели -> Создаете миграцию -> Применяете миграцию
- Коммитите миграции в репозиторий
- Коллеги применяют миграции после git pull

## Быстрый старт

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --ssl-keyfile ssl/key.pem --ssl-certfile ssl/cert.pem
```
### SSL Certificates
```bash
mkdir -p backend/ssl
openssl req -x509 -newkey rsa:4096 -nodes -out backend/ssl/cert.pem -keyout backend/ssl/key.pem -days 365\n
```


## .env файл - в корне backend
```
DATABASE_URL=postgresql+asyncpg://warehouse:warehouse123@localhost/warehouse_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
CORS_ORIGINS=http://localhost:3000, http://128.0.0.1:3000, 192.168.1.100:3000,https://localhost:3000,https://192.168.1.100:3000
DB_ECHO=True
```