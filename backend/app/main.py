import os
import ssl

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin
from app.api import auth, users, products
from app.core.config import settings
from app.admin import UserAdmin, ProductAdmin, AdminAuth, init_admin
from app.database.database import engine
from app.models.user import User
from app.models.product import Product

app = FastAPI(
    title="Warehouse Management System",
    version="1.0.0",
    debug=settings.DEBUG  # ✅ Включаем debug mode
)

# Добавляем middleware для сессий (нужно для SQLAdmin)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # React app
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)

# Setup SQLAdmin
init_admin(app)

@app.get("/")
async def root():
    return {"message": "Warehouse Management System API"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "debug": settings.DEBUG,
        "database_echo": settings.DB_ECHO
    }