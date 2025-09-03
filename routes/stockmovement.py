from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.stockmovement import StockMovementCreate, StockMovementRead
import crud.stockmovement as crud

router = APIRouter(prefix="/movements", tags=["Stock Movements"])


@router.post("/", response_model=StockMovementRead, summary="Create a stock movement")
async def create_movement(payload: StockMovementCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_movement(db, payload)


@router.get("/", response_model=List[StockMovementRead], summary="Get list of all stock movements")
async def list_movements(db: AsyncSession = Depends(get_db)):
    return await crud.list_movements(db)


@router.get("/{movement_id}", response_model=StockMovementRead, summary="Get movement by ID")
async def get_movement(movement_id: int, db: AsyncSession = Depends(get_db)):
    mv = await crud.get_movement(db, movement_id)
    if not mv:
        raise HTTPException(status_code=404, detail="Movement not found")
    return mv


@router.get("/product/{product_id}", response_model=List[StockMovementRead], summary="Movement by product")
async def movements_for_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.list_movements_for_product(db, product_id)


@router.get("/location/{location_id}", response_model=List[StockMovementRead], summary="Movement by location")
async def movements_for_location(location_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.list_movements_for_location(db, location_id)


@router.post("/{movement_id}/reversal", response_model=StockMovementRead, summary="Storno")
async def reversal(movement_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_reversal_movement(db, movement_id, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
