from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
import httpx

from app.core.database import get_db
from app.models.database_models import Product, Ingredient, ProductIngredient
from app.schemas.schemas import ProductCreate, ProductResponse
from app.services.recommendation_service import recommendation_service
from app.ai.ingredient_analyzer import ingredient_analyzer

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_vegan: Optional[bool] = None,
    is_cruelty_free: Optional[bool] = None,
    is_organic: Optional[bool] = None,
    min_rating: Optional[float] = None,
    max_rating: Optional[float] = None,
    min_safety_score: Optional[float] = None,
    max_safety_score: Optional[float] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db),
):
    query = select(Product)
    
    if category:
        query = query.where(Product.category == category)
    if brand:
        query = query.where(Product.brand == brand)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if is_vegan is not None:
        query = query.where(Product.is_vegan == is_vegan)
    if is_cruelty_free is not None:
        query = query.where(Product.is_cruelty_free == is_cruelty_free)
    if is_organic is not None:
        query = query.where(Product.is_organic == is_organic)
    if min_rating is not None:
        query = query.where(Product.rating >= min_rating)
    if max_rating is not None:
        query = query.where(Product.rating <= max_rating)
    if min_safety_score is not None:
        query = query.where(Product.safety_score >= min_safety_score)
    if max_safety_score is not None:
        query = query.where(Product.safety_score <= max_safety_score)

    if sort_by:
        if sort_by == "rating":
            sort_column = Product.rating
        elif sort_by == "price":
            sort_column = Product.price
        elif sort_by == "safety_score":
            sort_column = Product.safety_score
        elif sort_by == "review_count":
            sort_column = Product.review_count
        else:
            sort_column = Product.created_at

        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(Product.created_at.desc())
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = Product(**product_data.model_dump())
    db.add(product)
    await db.flush()
    await db.refresh(product)
    return product


@router.get("/search/{query}")
async def search_products(
    query: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Product).where(
            Product.name.ilike(f"%{query}%") | Product.brand.ilike(f"%{query}%")
        ).limit(10)
    )
    products = result.scalars().all()
    return {"products": products, "count": len(products)}


@router.get("/barcode/{barcode}")
async def get_product_by_barcode(barcode: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.barcode == barcode))
    product = result.scalar_one_or_none()
    
    if product:
        return product
    
    # Try to fetch from OpenBeautyFacts
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://world.openbeautyfacts.org/api/v2/product/{barcode}.json",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                obf_product = data.get("product", {})
                
                if obf_product:
                    # Create product from OBF data
                    product = Product(
                        name=obf_product.get("product_name", "Unknown Product"),
                        brand=obf_product.get("brands", "Unknown"),
                        barcode=barcode,
                        description=obf_product.get("generic_name", ""),
                        image_url=obf_product.get("image_front_url", ""),
                        data_source="OpenBeautyFacts",
                        external_id=barcode,
                    )
                    db.add(product)
                    await db.flush()
                    await db.refresh(product)
                    return product
    except Exception:
        pass
    
    raise HTTPException(status_code=404, detail="Product not found")


@router.post("/scan")
async def scan_product(file: UploadFile = File(...)):
    """Scan product image to extract ingredients."""
    from app.ai.ocr_service import ocr_service
    
    contents = await file.read()
    result = ocr_service.extract_text_from_image(contents)
    
    if result["success"]:
        # Analyze extracted ingredients
        if result["ingredients"]:
            analysis = ingredient_analyzer.analyze_all(result["ingredients"])
            return {
                "success": True,
                "extracted_text": result["raw_text"],
                "ingredients": result["ingredients"],
                "analysis": analysis
            }
    
    return result
