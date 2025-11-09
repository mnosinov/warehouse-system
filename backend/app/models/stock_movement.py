from datetime import datetime

from app.database.database import Base


class StockMovement(Base):
    id: int
    product_id: int
    movement_type: str  # 'incoming', 'outgoing', 'adjustment'
    quantity: int
    user_id: int
    created_at: datetime
