from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from crud.user import create_user, get_user_by_username
from schemas.user import UserCreate, UserRead
from routes import routers

app = FastAPI()


@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    # existing username check
    existing_user = await get_user_by_username(session, payload.username)
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    user = await create_user(session, payload.username, payload.password, payload.role)
    return user

@app.get("/users/{username}", response_model=UserRead)
async def get_user_endpoint(
    username: str,
    session: AsyncSession = Depends(get_session),
):
    user = await get_user_by_username(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

for router in routers:
    app.include_router(router)