class InventoryCheck(Base):
    id: int
    product_id: int
    expected_quantity: int
    actual_quantity: int
    user_id: int
    checked_at: datetime
