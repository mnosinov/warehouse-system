from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin
from app.api import auth, users, products
from app.core.config import settings
from app.admin import UserAdmin, ProductAdmin, AdminAuth
from app.database.database import engine
from app.models.user import User
from app.models.product import Product

app = FastAPI(title="Warehouse Management System", version="1.0.0")

# Добавляем middleware для сессий (нужно для SQLAdmin)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)

# Setup SQLAdmin
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)

@app.get("/")
async def root():
    return {"message": "Warehouse Management System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}