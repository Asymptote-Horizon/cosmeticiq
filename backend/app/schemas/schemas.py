from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class SkinType(str, Enum):
    DRY = "dry"
    OILY = "oily"
    COMBINATION = "combination"
    SENSITIVE = "sensitive"
    ACNE_PRONE = "acne_prone"
    NORMAL = "normal"


class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserProfileUpdate(BaseModel):
    skin_type: Optional[SkinType] = None
    age: Optional[int] = None
    climate: Optional[str] = None
    city: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    allergies: Optional[List[str]] = None
    concerns: Optional[List[str]] = None
    is_pregnant: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_cruelty_free: Optional[bool] = None
    hormonal_concerns: Optional[List[str]] = None


class ProductCreate(BaseModel):
    name: str
    brand: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: str = "USD"
    barcode: Optional[str] = None
    image_url: Optional[str] = None
    is_vegan: bool = False
    is_cruelty_free: bool = False
    is_organic: bool = False


class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    category: Optional[str]
    subcategory: Optional[str]
    description: Optional[str]
    price: Optional[float]
    currency: str
    barcode: Optional[str]
    image_url: Optional[str]
    rating: float
    review_count: int
    is_vegan: bool
    is_cruelty_free: bool
    is_organic: bool
    comedogenic_score: float
    fragrance_level: float
    alcohol_level: float
    scientific_score: float
    safety_score: float
    
    class Config:
        from_attributes = True


class IngredientResponse(BaseModel):
    id: int
    name: str
    inci_name: Optional[str]
    scientific_name: Optional[str]
    description: Optional[str]
    safety_score: float
    safety_status: str
    is_comedogenic: bool
    comedogenic_rating: float
    is_fragrance: bool
    is_allergen: bool
    is_endocrine_disruptor: bool
    is_pregnancy_unsafe: bool
    is_microplastic: bool
    is_animal_derived: bool
    is_irritant: bool
    ewg_score: float
    fda_status: Optional[str]
    eu_approved: bool
    functions: List[str]
    warnings: List[str]
    
    class Config:
        from_attributes = True


class FuzzyRuleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    conditions: Dict[str, Any]
    output: Dict[str, Any]
    weight: float
    is_active: bool
    category: Optional[str]
    
    class Config:
        from_attributes = True


class FuzzyInput(BaseModel):
    skin_type: str
    age: int
    climate: str
    budget: float
    ingredient_safety: float
    comedogenic_rating: float
    fragrance_level: float
    alcohol_presence: float
    product_rating: float
    scientific_evidence: float
    dermatologist_approval: float
    user_preferences: Dict[str, Any] = {}


class FuzzyOutput(BaseModel):
    suitability_score: float
    confidence: float
    triggered_rules: List[Dict[str, Any]]
    linguistic_output: str
    membership_values: Dict[str, float]


class RecommendationRequest(BaseModel):
    product_id: Optional[int] = None
    barcode: Optional[str] = None
    image_url: Optional[str] = None
    ingredients_text: Optional[str] = None


class RecommendationResponse(BaseModel):
    product: ProductResponse
    fuzzy_output: FuzzyOutput
    explanation: str
    confidence_score: float
    ingredients_analysis: List[IngredientResponse]
    scientific_references: List[Dict[str, Any]]
    alternatives: List[ProductResponse]


class ProductCompareRequest(BaseModel):
    product_ids: List[int]


class ProductCompareResponse(BaseModel):
    products: List[ProductResponse]
    ingredient_comparison: Dict[str, Any]
    safety_comparison: Dict[str, Any]
    fuzzy_comparison: List[FuzzyOutput]
    recommendation: str


class ClaimAnalysisRequest(BaseModel):
    content: str
    product_name: Optional[str] = None
    influencer_id: Optional[int] = None


class ClaimAnalysisResponse(BaseModel):
    verdict: str
    confidence_score: float
    evidence: List[Dict[str, Any]]
    explanation: str
    scientific_references: List[Dict[str, Any]]


class IngredientAnalysisRequest(BaseModel):
    ingredients_text: str
    product_name: Optional[str] = None


class IngredientAnalysisResponse(BaseModel):
    ingredients: List[IngredientResponse]
    safety_score: float
    warnings: List[str]
    recommendations: List[str]
    scientific_summary: Dict[str, Any]


class DashboardResponse(BaseModel):
    skin_profile: Dict[str, Any]
    routine: Dict[str, Any]
    current_products: List[ProductResponse]
    warnings: List[str]
    weekly_analysis: Dict[str, Any]
    monthly_improvement: Dict[str, Any]
    budget_tracker: Dict[str, Any]


class AdminProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    is_flagged: Optional[bool] = None
    flag_reason: Optional[str] = None


class BrandCreate(BaseModel):
    company_name: str
    country: Optional[str] = None
    founded_year: Optional[int] = None
    parent_company: Optional[str] = None
    brand_type: Optional[str] = None
    cruelty_free: bool = False
    vegan_products: bool = False
    dermatologist_recommended: bool = False
    official_website: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    popularity_score: float = 0
    sustainability_score: float = 0
    average_price_range: Optional[str] = None


class BrandResponse(BaseModel):
    id: int
    company_name: str
    country: Optional[str]
    founded_year: Optional[int]
    parent_company: Optional[str]
    brand_type: Optional[str]
    cruelty_free: bool
    vegan_products: bool
    dermatologist_recommended: bool
    official_website: Optional[str]
    logo_url: Optional[str]
    description: Optional[str]
    popularity_score: float
    sustainability_score: float
    average_price_range: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class BrandListResponse(BaseModel):
    brands: List[BrandResponse]
    total: int
    page: int
    per_page: int
