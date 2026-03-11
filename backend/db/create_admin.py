"""Script to create an admin user."""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import async_session_maker, init_db
from db.models import AdminUser
from api.admin.auth import get_password_hash


async def create_admin_user(username: str, password: str):
    """Create an admin user in the database."""
    # Initialize database
    await init_db()

    async with async_session_maker() as session:
        # Check if user already exists
        from sqlalchemy import select

        result = await session.execute(
            select(AdminUser).where(AdminUser.username == username)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"User '{username}' already exists!")
            return

        # Create new admin user
        hashed_password = get_password_hash(password)
        admin_user = AdminUser(
            username=username, hashed_password=hashed_password, is_active=True
        )

        session.add(admin_user)
        await session.commit()
        print(f"Admin user '{username}' created successfully!")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python -m db.create_admin <username> <password>")
        print("Example: python -m db.create_admin admin mypassword123")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    asyncio.run(create_admin_user(username, password))
