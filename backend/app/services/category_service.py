"""Category service."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_categories(self) -> list[Category]:
        result = await self.db.execute(
            select(Category)
            .where(Category.is_active == True)
            .order_by(Category.sort_order)
        )
        return list(result.scalars().all())

    async def get_category_by_slug(self, slug: str):
        result = await self.db.execute(
            select(Category).where(Category.slug == slug)
        )
        return result.scalar_one_or_none()
