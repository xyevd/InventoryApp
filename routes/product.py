from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas.product import ProductRead, ProductCreate, ProductUpdate
from crud.product import create_product, get_product, get_products, update_product, delete_product
from database import get_session

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductRead)
async def create_product_endpoint(product_in: ProductCreate, db: AsyncSession = Depends(get_session)):
    return await create_product(db, product_in)

@router.get("/", response_model=List[ProductRead])
async def get_products_endpoint(db: AsyncSession = Depends(get_session)):
    return await get_products(db)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product_endpoint(product_id: int, db: AsyncSession = Depends(get_session)):
    product = await get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductRead)
async def update_product_endpoint(product_id: int, product_in: ProductUpdate, db: AsyncSession = Depends(get_session)):
    product = await update_product(db, product_id, product_in)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=dict)
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_session)):
    success = await delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"ok": True}
