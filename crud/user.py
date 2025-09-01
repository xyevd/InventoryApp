from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from passlib.hash import bcrypt


# create user
async def create_user(db: AsyncSession, username: str, password: str, role: str):
    if not username or len(username) > 50:
        print(f"{username} is too long or empty")
        return None
    if role not in ("Admin", "User"):
        print(f"{role} is not a valid role")
        return None
    if not password:
        print(f"{password} is empty")
        return None
    existing_user = await get_user_by_username(db, username)
    if existing_user:
        print(f"{username} is already exists")
        return None
    try:
        hashed_password = bcrypt.hash(password)
        new_user = User(username=username, password_hash=hashed_password, role=role)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        print(f"{username} is created")
        return new_user
    except IntegrityError:
        await db.rollback()
        raise ValueError(f"{username} already exists(race condition)")

# get user by id
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# get user by username
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

# update user
async def update_user(db: AsyncSession, user_id: int, new_username: str = None, new_password: str = None, new_role: str = None):
    user = await get_user_by_id(db, user_id)
    if not user:
        print(f"{user_id} does not exist")
        return None
    if new_username and (not new_username or len(new_username) > 50):
        print(f"{new_username} is too long or empty")
        return None
    if new_username and (new_username != user.username):
        existing_user = await get_user_by_username(db, new_username)
        if existing_user:
            print(f"{new_username} is already exists")
            return None
    if new_role and (new_role not in ("Admin", "User")):
        print(f"{new_role} is not a valid role")
        return None
    try:
        if new_username:
            user.username = new_username
        if new_password:
            user.password_hash = bcrypt.hash(new_password)
        if new_role:
            user.role = new_role
        await db.commit()
        await db.refresh(user)
        print(f"User with id {user_id} updated")
        return user
    except IntegrityError:
        await db.rollback()
        print(f"User with username '{new_username}' already exists(race condition)")
        return None

# delete user
async def delete_user(db: AsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    await db.delete(user)
    await db.commit()
    return True
