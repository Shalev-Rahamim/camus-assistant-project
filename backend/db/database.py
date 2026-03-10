import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from db.models import Base

logger = logging.getLogger(__name__)

# 1. Secret management and flexibility
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./campus_assistant.db")

# 2. Async Engine
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# 3. Session Factory
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def init_db() -> None:
    """
    Creates all database tables defined in the SQLAlchemy models.
    Uses run_sync to bridge the gap between async engine and sync metadata creation.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")
        raise


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency generator that provides an async database session.
    """
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session rollback due to error: {e}")
            raise
        finally:
            await session.close()
