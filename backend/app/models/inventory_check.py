from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base

class InventoryCheck(Base):
    id: int
    product_id: int
    expected_quantity: int
    actual_quantity: int
    user_id: int
    checked_at: datetime
