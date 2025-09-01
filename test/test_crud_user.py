import asyncio
from database import AsyncSessionLocal
from crud.user import create_user, get_user_by_id, update_user, delete_user, get_user_by_username


async def main():
    async with AsyncSessionLocal() as session:
        # create user
        user = await create_user(session, "abdula", "123456", "Admin")
        print("@@@@@@@@CRE:", user.id, user.username, user.role)

        # read user
        fetched_user = await get_user_by_id(session, user.id)
        print("@@@@@@@@GET:", fetched_user.username)
        fetched_user = await get_user_by_username(session, user.username)
        print("@@@@@@@@GET:", fetched_user.username)

        # upd user
        updated = await update_user(session, user.id, new_password="newpass", new_role="User")
        print("@@@@@@@@UPD:", updated.username, updated.role)

        # delete user
        deleted = await delete_user(session, user.id)
        print("@@@@@@@@DEL:", deleted)

asyncio.run(main())
