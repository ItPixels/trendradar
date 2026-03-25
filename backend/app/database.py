import os
import asyncpg
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


def _get_raw_url() -> str:
    """Convert SQLAlchemy URL to raw postgresql:// for asyncpg."""
    return _get_db_url().replace("postgresql+asyncpg://", "postgresql://")


def _create_engine():
    """Create engine with asyncpg connection creator that disables prepared statement cache.

    The key fix: use async_creator to create asyncpg connections with
    statement_cache_size=0, which is required for Supabase's pgbouncer
    transaction-mode pooler (port 6543). SQLAlchemy's connect_args
    don't reliably pass this setting through to asyncpg.
    """
    raw_url = _get_raw_url()

    async def creator():
        return await asyncpg.connect(raw_url, statement_cache_size=0)

    engine = create_async_engine(
        _get_db_url(),
        echo=False,
        poolclass=NullPool,
        async_creator=creator,
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
