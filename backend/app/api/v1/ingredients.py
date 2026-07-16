from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.models.database_models import Ingredient
from app.schemas.schemas import IngredientResponse, IngredientAnalysisRequest
from app.ai.ingredient_analyzer import ingredient_analyzer

router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.get("/", response_model=List[IngredientResponse])
async def list_ingredients(
    skip: int = 0,
    limit: int = 20,
    category: str = None,
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy import select
    query = select(Ingredient)
    if category:
        query = query.where(Ingredient.safety_status == category)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{ingredient_id}", response_model=IngredientResponse)
async def get_ingredient(ingredient_id: int, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(Ingredient).where(Ingredient.id == ingredient_id))
    ingredient = result.scalar_one_or_none()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.post("/analyze")
async def analyze_ingredients(request: IngredientAnalysisRequest):
    """Analyze ingredients from text."""
    analysis = ingredient_analyzer.analyze_all(request.ingredients_text)
    return analysis


@router.get("/search/{name}")
async def search_ingredient(name: str):
    """Search for ingredient information."""
    info = ingredient_analyzer.analyze_ingredient(name)
    return {
        "name": info.name,
        "inci_name": info.inci_name,
        "category": info.category.value,
        "safety_score": info.safety_score,
        "functions": info.functions,
        "warnings": info.warnings,
        "description": info.description,
        "is_comedogenic": info.is_comedogenic,
        "is_fragrance": info.is_fragrance,
        "is_allergen": info.is_allergen,
        "is_endocrine_disruptor": info.is_endocrine_disruptor,
        "is_pregnancy_unsafe": info.is_pregnancy_unsafe,
        "is_microplastic": info.is_microplastic,
    }
