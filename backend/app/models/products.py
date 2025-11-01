class Product(Base):
    id: int
    name: str
    description: str
    sku: str  # Артикул
    qr_code: str
    current_quantity: int
    created_at: datetime

