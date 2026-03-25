import os
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool


def _get_db_url() -> str:
    """Get database URL from env or settings."""
    url = os.environ.get("DATABASE_URL")
    if not url:
        from app.config import settings
        url = settings.database_url
    return url


def _create_engine():
    """Create engine compatible with Supabase pgbouncer transaction-mode pooler.

    Key settings for pgbouncer compatibility:
    - NullPool: no connection pooling on our side (pgbouncer handles it)
    - statement_cache_size=0: disable asyncpg's internal prepared statement cache
    - prepared_statement_cache_size=0: disable SQLAlchemy's prepared statement cache
    - prepared_statement_name_func: unique names per invocation to avoid
      "prepared statement already exists" collisions across pgbouncer connections
    """
    # Generate a unique prefix for this engine instance to avoid
    # prepared statement name collisions across Vercel warm starts
    prefix = uuid.uuid4().hex[:8]

    engine = create_async_engine(
        _get_db_url(),
        echo=False,
        poolclass=NullPool,
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
            "prepared_statement_name_func": lambda: f"_ps_{prefix}_{uuid.uuid4().hex[:8]}",
        },
    )
    return engine


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    engine = _create_engine()
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await engine.dispose()
