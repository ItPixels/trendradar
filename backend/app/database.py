import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

_engine = None
_async_session = None


def _get_db_url() -> str:
    """Get database URL from env or settings."""
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    from app.config import settings
    return settings.database_url


def get_engine():
    global _engine
    if _engine is None:
        db_url = _get_db_url()
        _engine = create_async_engine(
            db_url,
            echo=False,
            poolclass=NullPool,
            connect_args={
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
            },
        )
    return _engine


def get_session_maker():
    global _async_session
    if _async_session is None:
        _async_session = async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)
    return _async_session


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
