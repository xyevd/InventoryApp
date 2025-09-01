from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from models import Location
from schemas.location import LocationCreate

async def create_location(db: AsyncSession, location: LocationCreate) -> Location:
    new_location = Location(**location.model_dump())
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return new_location

async def get_locations(db: AsyncSession):
    result = await db.execute(select(Location))
    return result.scalars().all()

async def get_location_by_id(db: AsyncSession, location_id: int):
    result = await db.execute(select(Location).where(Location.id == location_id))
    return result.scalars().first()

async def delete_location(db: AsyncSession, location_id: int):
    location = await db.execute(select(Location).where(Location.id == location_id))
    if not location:
        return None
    await db.delete(location)
    await db.commit()
    return True