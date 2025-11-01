from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base

class Warehouse(Base):
    id: int
    name: str
    location: str
