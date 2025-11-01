from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    sku = Column(String(50), unique=True, index=True)  # Артикул
    qr_code = Column(String(100), unique=True)
    current_quantity = Column(Integer, default=0)
    min_quantity = Column(Integer, default=0)
    max_quantity = Column(Integer, default=1000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())