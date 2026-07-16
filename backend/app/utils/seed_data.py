"""Seed data for initial database population."""

FUZZY_RULES_SEED = [
    {
        "name": "Sensitive Skin + High Fragrance + High Alcohol",
        "description": "Products with high fragrance and alcohol are bad for sensitive skin",
        "conditions": {
            "skin_type_sensitive": "high",
            "fragrance_level": "high",
            "alcohol_presence": "high"
        },
        "output": {"suitability": "very_bad"},
        "weight": 1.0,
        "category": "safety"
    },
    {
        "name": "Sensitive Skin + Low Fragrance + Low Alcohol",
        "description": "Fragrance-free, alcohol-free products are excellent for sensitive skin",
        "conditions": {
            "skin_type_sensitive": "high",
            "fragrance_level": "low",
            "alcohol_presence": "low"
        },
        "output": {"suitability": "excellent"},
        "weight": 1.0,
        "category": "safety"
    },
    {
        "name": "Dry Skin + High Ingredient Safety",
        "description": "Safe ingredients work well for dry skin",
        "conditions": {
            "skin_type_dry": "high",
            "ingredient_safety": "safe"
        },
        "output": {"suitability": "good"},
        "weight": 0.9,
        "category": "suitability"
    },
    {
        "name": "Oily Skin + High Comedogenic",
        "description": "Comedogenic products should be avoided for oily skin",
        "conditions": {
            "skin_type_oily": "high",
            "comedogenic_rating": "high"
        },
        "output": {"suitability": "very_bad"},
        "weight": 1.0,
        "category": "acne"
    },
    {
        "name": "Acne Prone + No Comedogenic + No Fragrance",
        "description": "Non-comedogenic, fragrance-free products are ideal for acne-prone skin",
        "conditions": {
            "skin_type_acne": "high",
            "comedogenic_rating": "none",
            "fragrance_level": "none"
        },
        "output": {"suitability": "excellent"},
        "weight": 1.0,
        "category": "acne"
    },
    {
        "name": "High Budget + Strong Evidence + Full Dermatologist Approval",
        "description": "Premium products with scientific backing are excellent",
        "conditions": {
            "budget": "high",
            "scientific_evidence": "strong",
            "dermatologist_approval": "full"
        },
        "output": {"suitability": "excellent"},
        "weight": 0.8,
        "category": "quality"
    },
    {
        "name": "Low Budget + Unsafe Ingredients",
        "description": "Cheap products with unsafe ingredients are very bad",
        "conditions": {
            "budget": "low",
            "ingredient_safety": "unsafe"
        },
        "output": {"suitability": "very_bad"},
        "weight": 1.0,
        "category": "safety"
    },
    {
        "name": "Young Skin + Oily + No Comedogenic",
        "description": "Young oily skin benefits from non-comedogenic products",
        "conditions": {
            "age": "young",
            "skin_type_oily": "high",
            "comedogenic_rating": "none"
        },
        "output": {"suitability": "excellent"},
        "weight": 0.9,
        "category": "suitability"
    },
    {
        "name": "Mature Skin + Strong Evidence + Safe",
        "description": "Mature skin benefits from scientifically proven safe products",
        "conditions": {
            "age": "mature",
            "scientific_evidence": "strong",
            "ingredient_safety": "safe"
        },
        "output": {"suitability": "excellent"},
        "weight": 0.9,
        "category": "anti-aging"
    },
    {
        "name": "Humid Climate + Oily Skin + High Fragrance",
        "description": "Fragrant products are worse in humid climates for oily skin",
        "conditions": {
            "climate_humid": "high",
            "skin_type_oily": "high",
            "fragrance_level": "high"
        },
        "output": {"suitability": "very_bad"},
        "weight": 0.9,
        "category": "climate"
    },
]

DEFAULT_INGREDIENTS = [
    {
        "name": "Hyaluronic Acid",
        "inci_name": "Sodium Hyaluronate",
        "safety_score": 1.0,
        "safety_status": "safe",
        "is_comedogenic": False,
        "is_fragrance": False,
        "is_allergen": False,
        "is_endocrine_disruptor": False,
        "is_pregnancy_unsafe": False,
        "is_microplastic": False,
        "functions": ["humectant", "anti-aging", "moisturizer"],
        "description": "Powerful humectant that holds 1000x its weight in water"
    },
    {
        "name": "Retinol",
        "inci_name": "Retinol",
        "safety_score": 0.8,
        "safety_status": "safe",
        "is_comedogenic": False,
        "is_fragrance": False,
        "is_allergen": False,
        "is_endocrine_disruptor": False,
        "is_pregnancy_unsafe": True,
        "is_microplastic": False,
        "functions": ["anti-aging", "acne treatment", "brightening"],
        "description": "Gold standard anti-aging ingredient"
    },
    {
        "name": "Niacinamide",
        "inci_name": "Niacinamide",
        "safety_score": 0.95,
        "safety_status": "safe",
        "is_comedogenic": False,
        "is_fragrance": False,
        "is_allergen": False,
        "is_endocrine_disruptor": False,
        "is_pregnancy_unsafe": False,
        "is_microplastic": False,
        "functions": ["brightening", "pore minimizing", "anti-inflammatory"],
        "description": "Vitamin B3, excellent for pores and brightening"
    },
    {
        "name": "Salicylic Acid",
        "inci_name": "Salicylic Acid",
        "safety_score": 0.85,
        "safety_status": "safe",
        "is_comedogenic": False,
        "is_fragrance": False,
        "is_allergen": False,
        "is_endocrine_disruptor": False,
        "is_pregnancy_unsafe": True,
        "is_microplastic": False,
        "functions": ["exfoliant", "acne treatment", "pore cleanser"],
        "description": "BHA exfoliant, excellent for acne-prone skin"
    },
    {
        "name": "Paraben",
        "inci_name": "Methylparaben",
        "safety_score": 0.3,
        "safety_status": "hazardous",
        "is_comedogenic": False,
        "is_fragrance": False,
        "is_allergen": False,
        "is_endocrine_disruptor": True,
        "is_pregnancy_unsafe": True,
        "is_microplastic": False,
        "functions": ["preservative"],
        "description": "Controversial preservative with endocrine disruption concerns"
    },
    {
        "name": "Fragrance",
        "inci_name": "Parfum",
        "safety_score": 0.4,
        "safety_status": "moderate",
        "is_comedogenic": False,
        "is_fragrance": True,
        "is_allergen": True,
        "is_endocrine_disruptor": False,
        "is_pregnancy_unsafe": False,
        "is_microplastic": False,
        "functions": ["fragrance"],
        "description": "Synthetic fragrance, potential allergen"
    },
    {
        "name": "Glycerin",
        "inci_name": "Glycerin",
        "safety_score": 1.0,
        "safety_status": "safe",
        "is_comedogenic": False,
        "is_fragrance": False,
        "is_allergen": False,
        "is_endocrine_disruptor": False,
        "is_pregnancy_unsafe": False,
        "is_microplastic": False,
        "functions": ["humectant", "moisturizer"],
        "description": "Excellent humectant, draws moisture to skin"
    },
    {
        "name": "Ceramide",
        "inci_name": "Ceramide NP",
        "safety_score": 1.0,
        "safety_status": "safe",
        "is_comedogenic": False,
        "is_fragrance": False,
        "is_allergen": False,
        "is_endocrine_disruptor": False,
        "is_pregnancy_unsafe": False,
        "is_microplastic": False,
        "functions": ["moisturizer", "barrier repair"],
        "description": "Essential for skin barrier health"
    },
]
