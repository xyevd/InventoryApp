from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import ProductInLocation
from schemas.product_in_location import ProductInLocationCreate

async def create_product_in_location(db: AsyncSession, obj_in: ProductInLocationCreate):
    new_entry = ProductInLocation(**obj_in.model_dump())
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    return new_entry


async def get_product_in_location(db: AsyncSession, product_id: int, location_id: int):
    result = await db.execute(
        select(ProductInLocation).where(
            ProductInLocation.product_id == product_id,
            ProductInLocation.location_id == location_id
        )
    )
    return result.scalar_one_or_none()


async def list_in_location(db: AsyncSession, location_id: int):
    result = await db.execute(
        select(ProductInLocation).where(ProductInLocation.location_id == location_id)
    )
    return result.scalars().all()


async def get_all(db: AsyncSession):
    result = await db.execute(select(ProductInLocation))
    return result.scalars().all()


##async def list_locations_for_product(db: AsyncSession, product_id: int):
##    result = await db.execute(
##        select(ProductInLocation).where(ProductInLocation.product_id == product_id)
##    )
##    return result.scalars().all()
