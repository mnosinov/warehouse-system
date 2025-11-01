from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: str
    current_quantity: int = 0
    min_quantity: int = 0
    max_quantity: int = 1000


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    qr_code: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True