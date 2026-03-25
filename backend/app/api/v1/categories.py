"""Categories API endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.category_service import CategoryService

router = APIRouter()


@router.get("")
async def list_categories(db: AsyncSession = Depends(get_db)):
    """Get all active categories."""
    service = CategoryService(db)
    categories = await service.get_all_categories()
    return {"items": categories}


@router.get("/{slug}")
async def get_category(slug: str, db: AsyncSession = Depends(get_db)):
    """Get a category by slug."""
    service = CategoryService(db)
    category = await service.get_category_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
