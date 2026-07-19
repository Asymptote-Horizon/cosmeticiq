import base64
import hashlib
import io
import math
import random
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.database_models import User
from app.api.v1.auth import get_current_user
from app.schemas.schemas import UserResponse

router = APIRouter(prefix="/skin-analysis", tags=["Skin Digital Twin"])


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class SkinMetrics(BaseModel):
    acne: float = Field(..., ge=0, le=10)
    pigmentation: float = Field(..., ge=0, le=10)
    wrinkles: float = Field(..., ge=0, le=10)
    oiliness: float = Field(..., ge=0, le=10)
    redness: float = Field(..., ge=0, le=10)
    dark_circles: float = Field(..., ge=0, le=10)
    pores: float = Field(..., ge=0, le=10)


class ProductRecommendation(BaseModel):
    product_name: str
    reason: str
    category: str
    priority: int = Field(..., ge=1, le=5)


class SkinAnalysisResponse(BaseModel):
    skin_metrics: SkinMetrics
    skin_type_guess: str
    overall_health_score: float = Field(..., ge=0, le=100)
    dominant_concerns: List[str]
    skin_tone: str
    age_estimate: str
    recommendations: List[ProductRecommendation]
    analysis_id: str
    analyzed_at: datetime


class SkinAnalysisHistory(BaseModel):
    id: int
    image_thumbnail: Optional[str] = None
    analyzed_at: datetime
    metrics: SkinMetrics

    class Config:
        from_attributes = True


class SkinConcern(BaseModel):
    name: str
    description: str
    severity: str
    icon: str


class Base64ImageRequest(BaseModel):
    image_base64: str = Field(..., min_length=100)


# ---------------------------------------------------------------------------
# Helpers – image analysis heuristics
# ---------------------------------------------------------------------------

_SKIN_TONES = ["light", "medium", "tan", "dark"]
_AGE_ESTIMATES = ["teens", "20s", "30s", "40s", "50s+"]
_SKIN_TYPES = ["dry", "oily", "combination", "sensitive", "normal"]

_PRODUCT_CATALOG: Dict[str, List[Dict]] = {
    "acne": [
        {"product_name": "Salicylic Acid Cleanser 2%", "reason": "Beta-hydroxy acid penetrates pores to dissolve sebum and dead skin cells", "category": "cleanser", "priority": 1},
        {"product_name": "Niacinamide 10% + Zinc 1%", "reason": "Reduces sebum production and calms inflammation", "category": "serum", "priority": 2},
        {"product_name": "Benzoyl Peroxide Spot Treatment 2.5%", "reason": "Kills acne-causing bacteria with minimal irritation at low concentration", "category": "treatment", "priority": 3},
        {"product_name": "Non-comedogenic Moisturizer", "reason": "Hydrates without clogging pores; essential even for oily/acne-prone skin", "category": "moisturizer", "priority": 4},
    ],
    "pigmentation": [
        {"product_name": "Vitamin C Serum 15%", "reason": "Brightens skin and inhibits melanin production with antioxidant protection", "category": "serum", "priority": 1},
        {"product_name": "Alpha Arbutin 2%", "reason": "Gentle tyrosinase inhibitor that fades dark spots over time", "category": "serum", "priority": 2},
        {"product_name": "Retinol 0.3% Night Serum", "reason": "Accelerates cell turnover to fade hyperpigmentation", "category": "treatment", "priority": 3},
        {"product_name": "SPF 50 Broad Spectrum Sunscreen", "reason": "Prevents further pigmentation; critical when using actives", "category": "sunscreen", "priority": 1},
    ],
    "wrinkles": [
        {"product_name": "Retinol 0.5% Anti-Aging Cream", "reason": "Gold-standard ingredient for stimulating collagen production", "category": "treatment", "priority": 1},
        {"product_name": "Hyaluronic Acid Serum 2%", "reason": "Plumps skin by holding up to 1000x its weight in water", "category": "serum", "priority": 2},
        {"product_name": "Peptide Night Repair Cream", "reason": "Supports skin firmness and elasticity during overnight repair", "category": "moisturizer", "priority": 3},
        {"product_name": "SPF 50 Daily Sunscreen", "reason": "UV damage is the #1 cause of premature wrinkles", "category": "sunscreen", "priority": 1},
    ],
    "oiliness": [
        {"product_name": "Gel-based Cleanser", "reason": "Removes excess oil without stripping the skin barrier", "category": "cleanser", "priority": 1},
        {"product_name": "Niacinamide 10% Serum", "reason": "Regulates sebum production and minimizes the appearance of pores", "category": "serum", "priority": 2},
        {"product_name": "Lightweight Water-Gel Moisturizer", "reason": "Oil-free hydration signals skin to produce less oil", "category": "moisturizer", "priority": 3},
        {"product_name": "Clay Mask (Kaolin) 1x/week", "reason": "Absorbs excess sebum and detoxifies pores", "category": "mask", "priority": 4},
    ],
    "redness": [
        {"product_name": "Centella Asiatica Serum", "reason": "Soothes inflammation and strengthens skin barrier", "category": "serum", "priority": 1},
        {"product_name": "Azelaic Acid 10%", "reason": "Reduces redness and has anti-inflammatory and antibacterial properties", "category": "treatment", "priority": 2},
        {"product_name": "Fragrance-free Barrier Repair Cream", "reason": "Ceramide-rich formula calms reactive skin", "category": "moisturizer", "priority": 3},
    ],
    "dark_circles": [
        {"product_name": "Vitamin K Eye Cream", "reason": "Strengthens capillary walls and reduces blood pooling under eyes", "category": "eye_care", "priority": 1},
        {"product_name": "Caffeine Eye Serum", "reason": "Constricts blood vessels and reduces puffiness", "category": "eye_care", "priority": 2},
        {"product_name": "Retinol Eye Treatment 0.1%", "reason": "Thickens delicate under-eye skin over time", "category": "eye_care", "priority": 3},
    ],
    "pores": [
        {"product_name": "BHA Exfoliant 2% Salicylic Acid", "reason": "Chemically exfoliates inside the pore lining", "category": "exfoliant", "priority": 1},
        {"product_name": "Niacinamide 5% Toner", "reason": "Tightens the appearance of enlarged pores", "category": "toner", "priority": 2},
        {"product_name": "Retinol 0.3% Serum", "reason": "Promotes cell turnover to prevent pore congestion", "category": "treatment", "priority": 3},
    ],
}

_CONCERN_DESCRIPTIONS: List[SkinConcern] = [
    SkinConcern(name="acne", description="Active breakouts, blackheads, or whiteheads caused by clogged pores and bacteria", severity="moderate", icon="🔴"),
    SkinConcern(name="pigmentation", description="Dark spots, uneven skin tone, or melasma from sun damage or post-inflammatory hyperpigmentation", severity="moderate", icon="🟤"),
    SkinConcern(name="wrinkles", description="Fine lines and deep creases from collagen loss, UV exposure, and natural aging", severity="mild", icon="〰️"),
    SkinConcern(name="oiliness", description="Excess sebum production leading to shine, enlarged pores, and potential breakouts", severity="mild", icon="💧"),
    SkinConcern(name="redness", description="Facial redness, rosacea-like flushing, or general skin irritation and sensitivity", severity="moderate", icon="🟥"),
    SkinConcern(name="dark_circles", description="Periorbital hyperpigmentation and hollowing under the eyes", severity="mild", icon="👁️"),
    SkinConcern(name="pores", description="Enlarged or visible pores, often in the T-zone, from excess oil and loss of elasticity", severity="mild", icon="⚫"),
]


def _seed_from_image(img_bytes: bytes) -> float:
    """Deterministic float [0, 1) derived from image content."""
    digest = hashlib.sha256(img_bytes).digest()
    return int.from_bytes(digest[:4], "big") / 0xFFFFFFFF


def _clamp(value: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return round(max(lo, min(hi, value)), 1)


def _analyse_image(img_bytes: bytes) -> dict:
    """
    Heuristic image analysis. Uses PIL to extract real pixel statistics and
    maps them to plausible skin-analysis scores. A seeded hash adds controlled
    variation so different uploads of the same image still feel natural.
    """
    from PIL import Image
    import numpy as np

    img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    pixels = np.array(img, dtype=np.float32)

    # Basic stats
    width, height = img.size
    total_pixels = width * height
    avg_rgb = pixels.mean(axis=(0, 1))  # [R, G, B]
    brightness = avg_rgb.mean() / 255.0
    r, g, b = avg_rgb / 255.0

    # Color variance (pigmentation proxy)
    std_rgb = pixels.reshape(-1, 3).std(axis=0).mean() / 255.0

    # Warm-tone ratio (red + yellow dominance → redness / oiliness proxy)
    warm_ratio = (r * 0.6 + (1.0 - b) * 0.4)

    # Darkness level (dark circles proxy if top-third of image is darker)
    top_third = pixels[: height // 3, :, :]
    bottom_third = pixels[2 * height // 3 :, :, :]
    top_brightness = top_third.mean() / 255.0
    bottom_brightness = bottom_third.mean() / 255.0
    top_bottom_diff = bottom_brightness - top_brightness

    # Texture proxy: high-frequency content via gradient magnitude
    gray = pixels.mean(axis=2)
    gy, gx = np.gradient(gray)
    texture = np.sqrt(gx**2 + gy**2).mean() / 255.0

    # Deterministic seed from content + random jitter
    seed = _seed_from_image(img_bytes)
    jitter = lambda: (random.random() - 0.5) * 0.6  # ±0.3 range

    # --- Map to scores -------------------------------------------------------
    # Oiliness: brighter skin + warm tones → higher oiliness score
    oiliness = _clamp(3.0 + brightness * 4.0 + warm_ratio * 2.0 + jitter())

    # Acne: texture + moderate brightness → acne
    acne = _clamp(2.0 + texture * 6.0 + std_rgb * 2.0 + jitter())

    # Pigmentation: color variance is the strongest signal
    pigmentation = _clamp(1.5 + std_rgb * 7.0 + abs(warm_ratio - 0.5) * 3.0 + jitter())

    # Wrinkles: high texture + lower brightness → wrinkles
    wrinkles = _clamp(1.0 + texture * 5.0 + (1.0 - brightness) * 3.0 + jitter())

    # Redness: warm ratio + brightness
    redness = _clamp(1.5 + warm_ratio * 5.0 + std_rgb * 2.0 + jitter())

    # Dark circles: top-bottom brightness diff
    dark_circles = _clamp(1.0 + max(0, -top_bottom_diff) * 6.0 + (1.0 - top_brightness) * 3.0 + jitter())

    # Pores: texture + brightness (oilier skin → visible pores)
    pores = _clamp(2.0 + texture * 4.0 + brightness * 3.0 + jitter())

    # Skin tone guess from average R/G/B
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    if luminance > 0.72:
        skin_tone = "light"
    elif luminance > 0.52:
        skin_tone = "medium"
    elif luminance > 0.35:
        skin_tone = "tan"
    else:
        skin_tone = "dark"

    # Skin type heuristic
    if oiliness > 6.5 and pigmentation < 4:
        skin_type = "oily"
    elif oiliness < 3.5 and redness > 5:
        skin_type = "dry"
    elif oiliness > 5 and redness > 5:
        skin_type = "combination"
    elif redness > 6:
        skin_type = "sensitive"
    else:
        skin_type = "normal"

    # Age estimate from wrinkle + texture
    complexity = wrinkles * 0.5 + texture * 10
    if complexity < 2.5:
        age_estimate = "teens"
    elif complexity < 3.5:
        age_estimate = "20s"
    elif complexity < 5.0:
        age_estimate = "30s"
    elif complexity < 6.5:
        age_estimate = "40s"
    else:
        age_estimate = "50s+"

    # Overall health: inverse of mean concern scores
    scores = [acne, pigmentation, wrinkles, oiliness, redness, dark_circles, pores]
    avg_concern = sum(scores) / len(scores)
    overall_health = round(max(0, min(100, 100 - avg_concern * 10)), 1)

    return {
        "acne": acne,
        "pigmentation": pigmentation,
        "wrinkles": wrinkles,
        "oiliness": oiliness,
        "redness": redness,
        "dark_circles": dark_circles,
        "pores": pores,
        "skin_type": skin_type,
        "skin_tone": skin_tone,
        "age_estimate": age_estimate,
        "overall_health": overall_health,
    }


def _get_recommendations(metrics: dict) -> List[ProductRecommendation]:
    """Return prioritised product recommendations for the top concerns."""
    concern_scores = {
        k: v for k, v in metrics.items() if k in _PRODUCT_CATALOG
    }
    top_concerns = sorted(concern_scores, key=concern_scores.get, reverse=True)[:3]

    recommendations: List[ProductRecommendation] = []
    for concern in top_concerns:
        products = _PRODUCT_CATALOG[concern]
        for p in products:
            recommendations.append(ProductRecommendation(**p))

    # Re-sort by priority then deduplicate
    seen = set()
    unique: List[ProductRecommendation] = []
    for r in sorted(recommendations, key=lambda x: x.priority):
        if r.product_name not in seen:
            seen.add(r.product_name)
            unique.append(r)
    return unique[:10]


def _run_analysis(img_bytes: bytes) -> dict:
    """Orchestrate analysis and build full response payload."""
    result = _analyse_image(img_bytes)

    metrics = SkinMetrics(
        acne=result["acne"],
        pigmentation=result["pigmentation"],
        wrinkles=result["wrinkles"],
        oiliness=result["oiliness"],
        redness=result["redness"],
        dark_circles=result["dark_circles"],
        pores=result["pores"],
    )

    concern_scores = {
        k: v for k, v in result.items() if k in _PRODUCT_CATALOG
    }
    dominant = sorted(concern_scores, key=concern_scores.get, reverse=True)[:3]

    analysis_id = hashlib.md5(img_bytes[:4096]).hexdigest()[:12]

    return {
        "skin_metrics": metrics,
        "skin_type_guess": result["skin_type"],
        "overall_health_score": result["overall_health"],
        "dominant_concerns": dominant,
        "skin_tone": result["skin_tone"],
        "age_estimate": result["age_estimate"],
        "recommendations": _get_recommendations(result),
        "analysis_id": analysis_id,
        "analyzed_at": datetime.utcnow(),
    }


# ---------------------------------------------------------------------------
# Optional auth dependency
# ---------------------------------------------------------------------------

async def get_optional_user(
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = None,
) -> Optional[User]:
    """Attempt to resolve a user from the Bearer token; return None if absent."""
    if not token:
        return None
    try:
        from jose import JWTError, jwt
        from app.core.config import settings
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        result = await db.execute(select(User).where(User.id == int(user_id)))
        return result.scalar_one_or_none()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/analyze", response_model=SkinAnalysisResponse)
async def analyze_skin_upload(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Analyse a skin image uploaded as a multipart file."""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image (JPEG, PNG, etc.)")

    contents = await file.read()
    if len(contents) < 1024:
        raise HTTPException(status_code=400, detail="Image file is too small or corrupted")
    if len(contents) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image file exceeds 20 MB limit")

    try:
        payload = _run_analysis(contents)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Unable to process image: {str(exc)}")

    return SkinAnalysisResponse(**payload)


@router.post("/analyze-base64", response_model=SkinAnalysisResponse)
async def analyze_skin_base64(
    body: Base64ImageRequest,
    db: AsyncSession = Depends(get_db),
):
    """Analyse a base64-encoded skin image (e.g. from camera capture)."""
    try:
        img_bytes = base64.b64decode(body.image_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image data")

    if len(img_bytes) < 1024:
        raise HTTPException(status_code=400, detail="Image data is too small or corrupted")
    if len(img_bytes) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image data exceeds 20 MB limit")

    try:
        payload = _run_analysis(img_bytes)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Unable to process image: {str(exc)}")

    return SkinAnalysisResponse(**payload)


@router.get("/history", response_model=List[SkinAnalysisHistory])
async def get_analysis_history(
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = None,
):
    """Return past skin analyses for the authenticated user (optional auth)."""
    user = await get_optional_user(db=db, token=token)
    if user is None:
        return []

    from app.models.database_models import SkinHistory
    result = await db.execute(
        select(SkinHistory)
        .where(SkinHistory.user_id == user.id)
        .order_by(SkinHistory.recorded_at.desc())
        .limit(50)
    )
    records = result.scalars().all()

    history: List[SkinAnalysisHistory] = []
    for record in records:
        metrics_data = record.concerns if isinstance(record.concerns, dict) else {}
        history.append(
            SkinAnalysisHistory(
                id=record.id,
                image_thumbnail=record.image_url,
                analyzed_at=record.recorded_at or datetime.utcnow(),
                metrics=SkinMetrics(
                    acne=metrics_data.get("acne", 0),
                    pigmentation=metrics_data.get("pigmentation", 0),
                    wrinkles=metrics_data.get("wrinkles", 0),
                    oiliness=metrics_data.get("oiliness", 0),
                    redness=metrics_data.get("redness", 0),
                    dark_circles=metrics_data.get("dark_circles", 0),
                    pores=metrics_data.get("pores", 0),
                ),
            )
        )
    return history


@router.get("/concerns", response_model=List[SkinConcern])
async def get_skin_concerns():
    """Return all supported skin concerns with descriptions."""
    return _CONCERN_DESCRIPTIONS
