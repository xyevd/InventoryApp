from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Product
from schemas.product import ProductCreate, ProductUpdate
from typing import Optional

async def create_product(db: AsyncSession, product: ProductCreate):
    new_product = Product(
        name=product.name,
        price=product.price
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product

async def get_product(db: AsyncSession, product_id: int) -> Optional[Product]:
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def update_product(db: AsyncSession, product_id: int, product_in: ProductUpdate) -> Optional[Product]:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        return None

    if product_in.name is not None:
        product.name = product_in.name
    if product_in.price is not None:
        product.price = product_in.price

    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(db: AsyncSession, product_id: int) -> bool:
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        return False

    await db.delete(product)
    await db.commit()
    return True
