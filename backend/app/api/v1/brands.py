from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional, List

from app.core.database import get_db
from app.models.database_models import Brand
from app.schemas.schemas import BrandCreate, BrandResponse, BrandListResponse
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/brands", tags=["Brands"])


@router.get("/", response_model=BrandListResponse)
async def list_brands(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    sort_by: str = Query("popularity_score", regex="^(company_name|popularity_score|sustainability_score|founded_year|average_price_range)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Brand)
    count_query = select(func.count(Brand.id))

    query = query.order_by(getattr(Brand, sort_by).desc() if sort_order == "desc" else getattr(Brand, sort_by).asc())

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    brands = result.scalars().all()

    return BrandListResponse(brands=brands, total=total, page=page, per_page=per_page)


@router.get("/search")
async def search_brands(
    q: Optional[str] = None,
    country: Optional[str] = None,
    brand_type: Optional[str] = None,
    cruelty_free: Optional[bool] = None,
    vegan_products: Optional[bool] = None,
    dermatologist_recommended: Optional[bool] = None,
    average_price_range: Optional[str] = None,
    min_popularity: Optional[float] = None,
    min_sustainability: Optional[float] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    sort_by: str = Query("popularity_score", regex="^(company_name|popularity_score|sustainability_score|founded_year)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Brand)
    conditions = []

    if q:
        search_term = f"%{q}%"
        conditions.append(
            or_(
                Brand.company_name.ilike(search_term),
                Brand.description.ilike(search_term),
                Brand.parent_company.ilike(search_term),
            )
        )
    if country:
        conditions.append(Brand.country == country)
    if brand_type:
        conditions.append(Brand.brand_type == brand_type)
    if cruelty_free is not None:
        conditions.append(Brand.cruelty_free == cruelty_free)
    if vegan_products is not None:
        conditions.append(Brand.vegan_products == vegan_products)
    if dermatologist_recommended is not None:
        conditions.append(Brand.dermatologist_recommended == dermatologist_recommended)
    if average_price_range:
        conditions.append(Brand.average_price_range == average_price_range)
    if min_popularity is not None:
        conditions.append(Brand.popularity_score >= min_popularity)
    if min_sustainability is not None:
        conditions.append(Brand.sustainability_score >= min_sustainability)

    if conditions:
        query = query.where(*conditions)

    count_query = select(func.count(Brand.id))
    if conditions:
        count_query = count_query.where(*conditions)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    sort_column = getattr(Brand, sort_by)
    query = query.order_by(sort_column.desc() if sort_order == "desc" else sort_column.asc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    brands = result.scalars().all()

    return BrandListResponse(brands=brands, total=total, page=page, per_page=per_page)


@router.get("/filters")
async def get_filter_options(db: AsyncSession = Depends(get_db)):
    countries = await db.execute(select(Brand.country).distinct().where(Brand.country.isnot(None)).order_by(Brand.country))
    brand_types = await db.execute(select(Brand.brand_type).distinct().where(Brand.brand_type.isnot(None)).order_by(Brand.brand_type))
    price_ranges = await db.execute(select(Brand.average_price_range).distinct().where(Brand.average_price_range.isnot(None)).order_by(Brand.average_price_range))

    return {
        "countries": [r[0] for r in countries.fetchall()],
        "brand_types": [r[0] for r in brand_types.fetchall()],
        "price_ranges": [r[0] for r in price_ranges.fetchall()],
    }


@router.get("/{brand_id}", response_model=BrandResponse)
async def get_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@router.post("/", response_model=BrandResponse)
async def create_brand(brand_data: BrandCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).where(Brand.company_name == brand_data.company_name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Brand already exists")

    brand = Brand(**brand_data.model_dump())
    db.add(brand)
    await db.flush()
    await db.refresh(brand)
    return brand


@router.post("/bulk", response_model=BrandListResponse)
async def bulk_create_brands(brands_data: List[BrandCreate], db: AsyncSession = Depends(get_db)):
    created = []
    skipped = 0
    for bd in brands_data:
        result = await db.execute(select(Brand).where(Brand.company_name == bd.company_name))
        if result.scalar_one_or_none():
            skipped += 1
            continue
        brand = Brand(**bd.model_dump())
        db.add(brand)
        created.append(brand)

    await db.flush()
    for b in created:
        await db.refresh(b)

    return BrandListResponse(brands=created, total=len(created), page=1, per_page=len(created))


@router.put("/{brand_id}", response_model=BrandResponse)
async def update_brand(brand_id: int, brand_data: BrandCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    for key, value in brand_data.model_dump(exclude_unset=True).items():
        setattr(brand, key, value)

    await db.flush()
    await db.refresh(brand)
    return brand


@router.delete("/{brand_id}")
async def delete_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    await db.delete(brand)
    await db.flush()
    return {"message": "Brand deleted successfully"}
