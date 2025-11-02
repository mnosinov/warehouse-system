from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.core.dependencies import require_admin, require_operator
import uuid

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductResponse])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_operator)
):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    products = result.scalars().all()
    return products

@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    # Проверяем, существует ли продукт с таким SKU
    result = await db.execute(select(Product).where(Product.sku == product_data.sku))
    existing_product = result.scalar_one_or_none()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )

    # Генерируем QR код (пока просто строку)
    qr_code = f"product:{uuid.uuid4()}"

    new_product = Product(
        name=product_data.name,
        description=product_data.description,
        sku=product_data.sku,
        qr_code=qr_code,
        current_quantity=product_data.current_quantity,
        min_quantity=product_data.min_quantity,
        max_quantity=product_data.max_quantity
    )

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_operator)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product