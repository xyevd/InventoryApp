from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from sqlalchemy.exc import IntegrityError
from models.stockmovement import StockMovement
from models.location import Location
from schemas.stockmovement import StockMovementCreate
from fastapi import HTTPException
from typing import Optional

async def create_movement(db: AsyncSession, data: StockMovementCreate) -> StockMovement:
    if data.from_loc is not None and data.to_loc is None:
        role = await db.scalar(select(Location.role).where(Location.id == data.from_loc))
        if role != "Store":
            raise HTTPException(400, "Role 'Store' is required for this operation.")

    if data.from_loc is None and data.to_loc is not None:
        role = await db.scalar(select(Location.role).where(Location.id == data.to_loc))
        if role != "Warehouse":
            raise HTTPException(400, "Role 'Warehouse' is required for this operation.")

    movement = StockMovement(**data.model_dump())
    db.add(movement)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(getattr(e.orig, "args", ["Integrity error"])[0]))
    await db.refresh(movement)
    return movement

async def list_movements(db: AsyncSession) -> Sequence[StockMovement]:
    result = await db.execute(select(StockMovement))
    return result.scalars().all()

async def list_movements_for_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(StockMovement).where(StockMovement.product_id == product_id)
    )
    return result.scalars().all()

async def list_movements_for_location(db: AsyncSession, location_id: int):
    result = await db.execute(
        select(StockMovement).where(
            (StockMovement.from_loc == location_id) | (StockMovement.to_loc == location_id)
        )
    )
    return result.scalars().all()

async def get_movement(db: AsyncSession, movement_id: int) -> Optional[StockMovement]:
    res = await db.execute(select(StockMovement).where(StockMovement.id == movement_id))
    return res.scalar_one_or_none()

async def create_reversal_movement(db: AsyncSession, movement_id: int, *,user_id: int,) -> StockMovement:
    original = await get_movement(db, movement_id)
    if not original:
        raise ValueError("Movement not found")

    reversed_payload = StockMovementCreate(
        user_id=user_id,
        product_id=original.product_id,
        from_loc=original.to_loc,
        to_loc=original.from_loc,
        quantity=original.quantity,
    )
    return await create_movement(db, reversed_payload)