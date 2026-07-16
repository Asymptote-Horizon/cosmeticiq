from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.database_models import Product, UserProfile, User
from app.schemas.schemas import (
    RecommendationRequest,
    ProductCompareRequest,
    FuzzyInput,
)
from app.services.recommendation_service import recommendation_service
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def _safe_skin_type(val):
    if val is None:
        return "normal"
    return val if isinstance(val, str) else val.value if hasattr(val, "value") else "normal"


@router.post("/analyze")
async def analyze_product(
    request: RecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if request.product_id:
        result = await db.execute(
            select(Product).where(Product.id == request.product_id)
        )
        product = result.scalar_one_or_none()
    elif request.barcode:
        result = await db.execute(
            select(Product).where(Product.barcode == request.barcode)
        )
        product = result.scalar_one_or_none()
    else:
        raise HTTPException(status_code=400, detail="Provide product_id or barcode")

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=400, detail="Please complete your profile first")

    product_data = {
        "id": product.id,
        "name": product.name,
        "brand": product.brand,
        "category": product.category,
        "price": product.price,
        "rating": product.rating or 3.0,
        "comedogenic_score": product.comedogenic_score or 0,
        "fragrance_level": product.fragrance_level or 0,
        "alcohol_level": product.alcohol_level or 0,
        "scientific_score": product.scientific_score or 0.5,
        "ingredients": "",
    }

    user_data = {
        "skin_type": _safe_skin_type(profile.skin_type),
        "age": profile.age or 30,
        "climate": profile.climate or "moderate",
        "budget_max": profile.budget_max or 200,
        "concerns": profile.concerns or [],
        "is_pregnant": profile.is_pregnant,
        "is_vegan": profile.is_vegan,
    }

    recommendation = recommendation_service.get_recommendation(product_data, user_data)

    analysis = recommendation["ingredients_analysis"]
    ingredients_list = []
    for ing in analysis.get("ingredients", []):
        if hasattr(ing, "__dict__"):
            ingredients_list.append({
                "name": ing.name,
                "safety_score": ing.safety_score,
                "category": ing.category.value if hasattr(ing.category, "value") else str(ing.category),
                "warnings": ing.warnings,
                "functions": ing.functions,
                "is_comedogenic": ing.is_comedogenic,
                "is_fragrance": ing.is_fragrance,
                "is_allergen": ing.is_allergen,
                "is_endocrine_disruptor": ing.is_endocrine_disruptor,
                "is_pregnancy_unsafe": ing.is_pregnancy_unsafe,
                "is_irritant": ing.is_irritant,
            })
        elif isinstance(ing, dict):
            ingredients_list.append(ing)
        else:
            ingredients_list.append({"name": str(ing), "safety_score": 0.5, "category": "unknown"})

    return {
        "product": {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "category": product.category,
            "price": product.price,
            "rating": product.rating,
            "image_url": product.image_url,
        },
        "fuzzy_output": recommendation["fuzzy_output"],
        "explanation": recommendation["explanation"],
        "confidence_score": recommendation["confidence_score"],
        "ingredients_analysis": ingredients_list,
        "scientific_references": [],
        "alternatives": [],
    }


@router.post("/compare")
async def compare_products(
    request: ProductCompareRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    products = []
    for product_id in request.product_ids:
        result = await db.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        if product:
            products.append(product)

    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    user_data = {
        "skin_type": _safe_skin_type(profile.skin_type) if profile else "normal",
        "age": profile.age if profile else 30,
        "climate": profile.climate if profile else "moderate",
        "budget_max": profile.budget_max if profile else 200,
    }

    products_data = []
    for product in products:
        products_data.append({
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "rating": product.rating or 3.0,
            "ingredients": "",
            "comedogenic_score": product.comedogenic_score or 0,
            "fragrance_level": product.fragrance_level or 0,
            "alcohol_level": product.alcohol_level or 0,
            "scientific_score": product.scientific_score or 0.5,
            "safety_score": product.safety_score or 0.5,
        })

    comparison = recommendation_service.compare_products(products_data, user_data)

    safe_products = []
    for rec in comparison.get("products", []):
        p = rec.get("product", {})
        safe_products.append({
            "product": {
                "id": p.get("id"),
                "name": p.get("name"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating", 3.0),
            },
            "fuzzy_output": rec.get("fuzzy_output", {}),
            "explanation": rec.get("explanation", ""),
            "confidence_score": rec.get("confidence_score", 0.5),
            "ingredients_analysis": rec.get("ingredients_analysis", {}),
        })

    return {
        "products": safe_products,
        "recommendation": comparison.get("recommendation", ""),
    }


@router.post("/compare-public")
async def compare_products_public(
    request: ProductCompareRequest,
    db: AsyncSession = Depends(get_db),
):
    products = []
    for product_id in request.product_ids:
        result = await db.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        if product:
            products.append(product)

    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    user_data = {
        "skin_type": "normal",
        "age": 30,
        "climate": "moderate",
        "budget_max": 200,
    }

    products_data = []
    for product in products:
        products_data.append({
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "rating": product.rating or 3.0,
            "ingredients": "",
            "comedogenic_score": product.comedogenic_score or 0,
            "fragrance_level": product.fragrance_level or 0,
            "alcohol_level": product.alcohol_level or 0,
            "scientific_score": product.scientific_score or 0.5,
            "safety_score": product.safety_score or 0.5,
        })

    comparison = recommendation_service.compare_products(products_data, user_data)

    safe_products = []
    for rec in comparison.get("products", []):
        p = rec.get("product", {})
        safe_products.append({
            "product": {
                "id": p.get("id"),
                "name": p.get("name"),
                "brand": p.get("brand"),
                "price": p.get("price"),
                "rating": p.get("rating", 3.0),
            },
            "fuzzy_output": rec.get("fuzzy_output", {}),
            "explanation": rec.get("explanation", ""),
            "confidence_score": rec.get("confidence_score", 0.5),
            "ingredients_analysis": rec.get("ingredients_analysis", {}),
        })

    return {
        "products": safe_products,
        "recommendation": comparison.get("recommendation", ""),
    }


@router.post("/fuzzy-evaluate")
async def fuzzy_evaluate(input_data: FuzzyInput):
    from app.decision_engine.fuzzy_engine import fuzzy_engine

    fuzzy_input = {
        'skin_type_dry': 1.0 if input_data.skin_type == 'dry' else 0.0,
        'skin_type_oily': 1.0 if input_data.skin_type == 'oily' else 0.0,
        'skin_type_sensitive': 1.0 if input_data.skin_type == 'sensitive' else 0.0,
        'skin_type_acne': 1.0 if input_data.skin_type == 'acne_prone' else 0.0,
        'age': input_data.age,
        'climate_humid': 0.9 if input_data.climate == 'humid' else 0.1,
        'climate_dry': 0.9 if input_data.climate == 'dry' else 0.1,
        'climate_cold': 0.9 if input_data.climate == 'cold' else 0.1,
        'budget': input_data.budget,
        'ingredient_safety': input_data.ingredient_safety,
        'comedogenic_rating': input_data.comedogenic_rating,
        'fragrance_level': input_data.fragrance_level,
        'alcohol_presence': input_data.alcohol_presence,
        'product_rating': input_data.product_rating,
        'scientific_evidence': input_data.scientific_evidence,
        'dermatologist_approval': input_data.dermatologist_approval,
    }

    result = fuzzy_engine.evaluate(fuzzy_input)
    return result
