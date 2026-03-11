"""
Migration script to add session_id column to conversations table.
Run this once to update existing database.
"""

import asyncio
import logging
from sqlalchemy import text
from db import engine

logger = logging.getLogger(__name__)


async def migrate_add_session_id():
    """Add session_id column to conversations table if it doesn't exist."""
    try:
        async with engine.begin() as conn:
            # Check if column exists
            result = await conn.execute(text("PRAGMA table_info(conversations)"))
            columns = [row[1] for row in result.fetchall()]

            if "session_id" not in columns:
                logger.info("Adding session_id column to conversations table...")

                # SQLite doesn't support ALTER TABLE ADD COLUMN with NOT NULL directly
                # So we'll add it as nullable first, then update existing rows, then make it NOT NULL
                # Actually, for SQLite, we can add it with a default value

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
            else:
                logger.info("session_id column already exists in conversations table")

    except Exception as e:
        logger.error(f"Error migrating database: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(migrate_add_session_id())
    print("Migration completed!")
