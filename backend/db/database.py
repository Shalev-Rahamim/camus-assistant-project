import os
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from db.models import Base

logger = logging.getLogger(__name__)

# 1. Secret management and flexibility
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./campus_assistant.db")

# 2. Async Engine
engine = create_async_engine(DATABASE_URL, echo=False)

# 3. Session Factory
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def init_db() -> None:
    """
    Creates all database tables defined in the SQLAlchemy models.
    Uses run_sync to bridge the gap between async engine and sync metadata creation.
    Also runs migrations if needed.
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully.")

        # Run migration to add session_id if needed
        try:
            from sqlalchemy import text

            async with engine.begin() as conn:
                # Check if column exists
                result = await conn.execute(text("PRAGMA table_info(conversations)"))
                columns = [row[1] for row in result.fetchall()]

                if "session_id" not in columns:
                    logger.info("Adding session_id column to conversations table...")
                    # Add column with default value
                    await conn.execute(
                        text(
                            "ALTER TABLE conversations ADD COLUMN session_id VARCHAR(255) DEFAULT 'migrated_session'"
                        )
                    )
                    # Create index
                    await conn.execute(
                        text(
                            "CREATE INDEX IF NOT EXISTS ix_conversations_session_id ON conversations(session_id)"
                        )
                    )
                    logger.info(
                        "Successfully added session_id column to conversations table"
                    )
        except Exception as migration_error:
            # If conversations table doesn't exist yet, that's fine
            if "no such table" not in str(migration_error).lower():
                logger.warning(f"Migration warning: {migration_error}")
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
