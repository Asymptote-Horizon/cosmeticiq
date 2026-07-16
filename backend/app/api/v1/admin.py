from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.models.database_models import Product, Ingredient, User, FuzzyRule, Claim
from app.api.v1.auth import get_current_user
from app.schemas.schemas import AdminProductUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


async def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


@router.get("/stats")
async def get_admin_stats(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    products_count = await db.scalar(select(func.count(Product.id)))
    users_count = await db.scalar(select(func.count(User.id)))
    ingredients_count = await db.scalar(select(func.count(Ingredient.id)))
    rules_count = await db.scalar(select(func.count(FuzzyRule.id)))
    claims_count = await db.scalar(select(func.count(Claim.id)))
    
    return {
        "products": products_count or 0,
        "users": users_count or 0,
        "ingredients": ingredients_count or 0,
        "fuzzy_rules": rules_count or 0,
        "claims": claims_count or 0,
    }


@router.get("/products")
async def list_all_products(
    skip: int = 0,
    limit: int = 50,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    products = result.scalars().all()
    return {"products": products, "count": len(products)}


@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    update_data: AdminProductUpdate,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    await db.flush()
    return {"message": "Product updated"}


@router.get("/users")
async def list_all_users(
    skip: int = 0,
    limit: int = 50,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return {"users": users, "count": len(users)}


@router.get("/rules")
async def list_fuzzy_rules(
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(FuzzyRule))
    rules = result.scalars().all()
    return {"rules": rules, "count": len(rules)}


@router.post("/rules")
async def create_fuzzy_rule(
    name: str,
    conditions: dict,
    output: dict,
    admin: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    rule = FuzzyRule(
        name=name,
        conditions=conditions,
        output=output,
        is_active=True,
    )
    db.add(rule)
    await db.flush()
    return {"message": "Rule created", "id": rule.id}
