import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool


def _get_db_url() -> str:
    """Get database URL from env or settings."""
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    from app.config import settings
    return settings.database_url


def _create_engine():
    """Create a fresh engine every time — required for serverless + pgbouncer transaction mode.

    With NullPool there is no connection pool, so engine creation is cheap.
    A fresh engine avoids stale dialect state on Vercel warm starts that causes
    DuplicatePreparedStatementError with Supabase transaction-mode pooler.
    """
    db_url = _get_db_url()
    engine = create_async_engine(
        db_url,
        echo=False,
        poolclass=NullPool,
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
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
