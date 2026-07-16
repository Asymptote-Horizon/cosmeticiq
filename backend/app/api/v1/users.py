from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.database_models import UserProfile, User
from app.schemas.schemas import UserProfileUpdate
from app.api.v1.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        return {"message": "No profile found", "setup_required": True}

    skin_type = profile.skin_type if isinstance(profile.skin_type, str) else (profile.skin_type.value if profile.skin_type else "normal")

    return {
        "skin_type": skin_type,
        "age": profile.age,
        "climate": profile.climate,
        "city": profile.city,
        "budget_min": profile.budget_min,
        "budget_max": profile.budget_max,
        "allergies": profile.allergies or [],
        "concerns": profile.concerns or [],
        "is_pregnant": profile.is_pregnant,
        "is_vegan": profile.is_vegan,
        "is_cruelty_free": profile.is_cruelty_free,
        "hormonal_concerns": profile.hormonal_concerns or [],
    }


@router.put("/profile")
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)
        await db.flush()

    update_data = profile_data.model_dump(exclude_unset=True)

    if "skin_type" in update_data and update_data["skin_type"]:
        profile.skin_type = update_data["skin_type"]
        del update_data["skin_type"]

    for key, value in update_data.items():
        setattr(profile, key, value)

    await db.flush()
    await db.refresh(profile)

    skin_type = profile.skin_type if isinstance(profile.skin_type, str) else (profile.skin_type.value if profile.skin_type else "normal")

    return {
        "message": "Profile updated successfully",
        "skin_type": skin_type,
        "age": profile.age,
        "climate": profile.climate,
    }


@router.get("/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == current_user.id)
    )
    profile = result.scalar_one_or_none()

    skin_type = "normal"
    age = 30
    concerns = []
    budget_max = 200

    if profile:
        skin_type = profile.skin_type if isinstance(profile.skin_type, str) else (profile.skin_type.value if profile.skin_type else "normal")
        age = profile.age or 30
        concerns = profile.concerns or []
        budget_max = profile.budget_max or 200

    return {
        "skin_profile": {
            "skin_type": skin_type,
            "age": age,
            "concerns": concerns,
        },
        "routine": profile.routine if profile else {},
        "current_products": [],
        "warnings": [],
        "weekly_analysis": {
            "hydration": 78,
            "clarity": 82,
            "sensitivity": 25,
        },
        "monthly_improvement": {
            "hydration_change": "+5%",
            "clarity_change": "+8%",
            "sensitivity_change": "-3%",
        },
        "budget_tracker": {
            "monthly_budget": budget_max,
            "spent": 90,
            "remaining": max(budget_max - 90, 0),
            "total_saved": 245,
        },
    }
