from typing import Dict, List, Any, Optional
import re
from dataclasses import dataclass
from enum import Enum


class IngredientCategory(Enum):
    SAFE = "safe"
    MODERATE = "moderate"
    HAZARDOUS = "hazardous"
    UNKNOWN = "unknown"


@dataclass
class IngredientInfo:
    name: str
    inci_name: str
    category: IngredientCategory
    safety_score: float
    is_comedogenic: bool
    comedogenic_rating: float
    is_fragrance: bool
    is_allergen: bool
    is_endocrine_disruptor: bool
    is_pregnancy_unsafe: bool
    is_microplastic: bool
    is_animal_derived: bool
    is_irritant: bool
    functions: List[str]
    warnings: List[str]
    description: str


# Comprehensive ingredient database
INGREDIENT_DATABASE = {
    # Safe Ingredients
    "water": IngredientInfo(
        name="Water", inci_name="Aqua", category=IngredientCategory.SAFE,
        safety_score=1.0, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["solvent", "base"],
        warnings=[], description="Base ingredient, safe for all skin types"
    ),
    "glycerin": IngredientInfo(
        name="Glycerin", inci_name="Glycerin", category=IngredientCategory.SAFE,
        safety_score=1.0, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["humectant", "moisturizer"],
        warnings=[], description="Excellent humectant, draws moisture to skin"
    ),
    "hyaluronic acid": IngredientInfo(
        name="Hyaluronic Acid", inci_name="Sodium Hyaluronate", category=IngredientCategory.SAFE,
        safety_score=1.0, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["humectant", "anti-aging", "moisturizer"],
        warnings=[], description="Powerful humectant, holds 1000x its weight in water"
    ),
    "ceramide": IngredientInfo(
        name="Ceramides", inci_name="Ceramide NP", category=IngredientCategory.SAFE,
        safety_score=1.0, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["moisturizer", "barrier repair", "anti-aging"],
        warnings=[], description="Essential for skin barrier health"
    ),
    "niacinamide": IngredientInfo(
        name="Niacinamide", inci_name="Niacinamide", category=IngredientCategory.SAFE,
        safety_score=0.95, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["brightening", "pore minimizing", "anti-inflammatory"],
        warnings=[], description="Vitamin B3, excellent for pores and brightening"
    ),
    "salicylic acid": IngredientInfo(
        name="Salicylic Acid", inci_name="Salicylic Acid", category=IngredientCategory.SAFE,
        safety_score=0.85, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=True, is_microplastic=False, is_animal_derived=False,
        is_irritant=True, functions=["exfoliant", "acne treatment", "pore cleanser"],
        warnings=["Not recommended during pregnancy", "May cause dryness"],
        description="BHA exfoliant, excellent for acne-prone skin"
    ),
    "retinol": IngredientInfo(
        name="Retinol", inci_name="Retinol", category=IngredientCategory.SAFE,
        safety_score=0.8, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=True, is_microplastic=False, is_animal_derived=False,
        is_irritant=True, functions=["anti-aging", "acne treatment", "brightening"],
        warnings=["Not recommended during pregnancy", "Use sunscreen", "May cause irritation"],
        description="Gold standard anti-aging ingredient"
    ),
    "vitamin c": IngredientInfo(
        name="Vitamin C", inci_name="Ascorbic Acid", category=IngredientCategory.SAFE,
        safety_score=0.9, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=True, functions=["antioxidant", "brightening", "collagen booster"],
        warnings=["May cause irritation in sensitive skin", "Use sunscreen"],
        description="Powerful antioxidant for brightening and protection"
    ),
    "aloe vera": IngredientInfo(
        name="Aloe Vera", inci_name="Aloe Barbadensis", category=IngredientCategory.SAFE,
        safety_score=0.95, is_comedogenic=False, comedogenic_rating=1,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["soothing", "moisturizer", "healing"],
        warnings=[], description="Natural soothing and healing ingredient"
    ),
    "centella asiatica": IngredientInfo(
        name="Centella Asiatica", inci_name="Centella Asiatica Extract", category=IngredientCategory.SAFE,
        safety_score=0.95, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["soothing", "healing", "anti-aging", "collagen booster"],
        warnings=[], description="Cica, excellent for barrier repair and soothing"
    ),
    
    # Moderate Ingredients
    "alcohol denat": IngredientInfo(
        name="Alcohol Denat", inci_name="Alcohol Denat.", category=IngredientCategory.MODERATE,
        safety_score=0.5, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=True, functions=["solvent", "preservative", "penetration enhancer"],
        warnings=["Can be drying", "May irritate sensitive skin", "Avoid on dry skin"],
        description="Drying alcohol, can be harsh on skin"
    ),
    "sodium laureth sulfate": IngredientInfo(
        name="Sodium Laureth Sulfate", inci_name="Sodium Laureth Sulfate", category=IngredientCategory.MODERATE,
        safety_score=0.4, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=True, functions=["surfactant", "cleansing agent"],
        warnings=["Can be drying", "May cause irritation"],
        description="Common surfactant, can be stripping"
    ),
    "parfum": IngredientInfo(
        name="Fragrance", inci_name="Parfum", category=IngredientCategory.MODERATE,
        safety_score=0.4, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=True, is_allergen=True, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=True, functions=["fragrance"],
        warnings=["Can cause allergies", "May irritate sensitive skin", "Common allergen"],
        description="Synthetic fragrance, potential allergen"
    ),
    "phenoxyethanol": IngredientInfo(
        name="Phenoxyethanol", inci_name="Phenoxyethanol", category=IngredientCategory.MODERATE,
        safety_score=0.6, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=False, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["preservative"],
        warnings=["May cause irritation in very sensitive skin"],
        description="Common preservative, generally safe"
    ),
    
    # Hazardous Ingredients
    "paraben": IngredientInfo(
        name="Parabens", inci_name="Methylparaben", category=IngredientCategory.HAZARDOUS,
        safety_score=0.3, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=True,
        is_pregnancy_unsafe=True, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=["preservative"],
        warnings=["Endocrine disruptor", "Avoid during pregnancy", "Controversial safety"],
        description="Controversial preservatives with endocrine concerns"
    ),
    "formaldehyde": IngredientInfo(
        name="Formaldehyde", inci_name="Formaldehyde", category=IngredientCategory.HAZARDOUS,
        safety_score=0.1, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=True, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=True, is_microplastic=False, is_animal_derived=False,
        is_irritant=True, functions=["preservative"],
        warnings=["Carcinogen", "Strong irritant", "Avoid completely"],
        description="Known carcinogen, avoid completely"
    ),
    "lead": IngredientInfo(
        name="Lead", inci_name="Lead", category=IngredientCategory.HAZARDOUS,
        safety_score=0.0, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=True,
        is_pregnancy_unsafe=True, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=[],
        warnings=["Neurotoxin", "Avoid completely", "Toxic"],
        description="Toxic heavy metal, avoid completely"
    ),
    "mercury": IngredientInfo(
        name="Mercury", inci_name="Mercury", category=IngredientCategory.HAZARDOUS,
        safety_score=0.0, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=False,
        is_pregnancy_unsafe=True, is_microplastic=False, is_animal_derived=False,
        is_irritant=False, functions=[],
        warnings=["Neurotoxin", "Toxic", "Illegal in cosmetics"],
        description="Toxic heavy metal, illegal in cosmetics"
    ),
    "microplastic": IngredientInfo(
        name="Microplastics", inci_name="Polyethylene", category=IngredientCategory.HAZARDOUS,
        safety_score=0.2, is_comedogenic=False, comedogenic_rating=0,
        is_fragrance=False, is_allergen=False, is_endocrine_disruptor=True,
        is_pregnancy_unsafe=False, is_microplastic=True, is_animal_derived=False,
        is_irritant=False, functions=["exfoliant", "texture enhancer"],
        warnings=["Environmental hazard", "May disrupt hormones", "Avoid for eco-conscious"],
        description="Microplastic particles, harmful to environment"
    ),
}


class IngredientAnalyzer:
    """Analyze cosmetic ingredients for safety and suitability."""
    
    def __init__(self):
        self.database = INGREDIENT_DATABASE
    
    def parse_ingredients(self, text: str) -> List[str]:
        """Parse ingredient list from text."""
        # Clean and normalize text
        text = text.strip()
        
        # Try comma-separated first
        if ',' in text:
            ingredients = [i.strip().lower() for i in text.split(',') if i.strip()]
        # Try newline separated
        elif '\n' in text:
            ingredients = [i.strip().lower() for i in text.split('\n') if i.strip()]
        # Try space separated (less reliable)
        else:
            # Common delimiters
            for delimiter in [';', '|', '/', ' and ']:
                if delimiter in text.lower():
                    ingredients = [i.strip().lower() for i in text.lower().split(delimiter) if i.strip()]
                    break
            else:
                # Try to split by common ingredient patterns
                ingredients = [text.strip().lower()]
        
        return ingredients
    
    def analyze_ingredient(self, name: str) -> IngredientInfo:
        """Analyze a single ingredient."""
        name_lower = name.lower().strip()
        
        # Check exact match
        if name_lower in self.database:
            return self.database[name_lower]
        
        # Check partial matches
        for key, info in self.database.items():
            if key in name_lower or name_lower in key:
                return info
        
        # Return unknown if not found
        return IngredientInfo(
            name=name.title(),
            inci_name=name.title(),
            category=IngredientCategory.UNKNOWN,
            safety_score=0.5,
            is_comedogenic=False,
            comedogenic_rating=0,
            is_fragrance=False,
            is_allergen=False,
            is_endocrine_disruptor=False,
            is_pregnancy_unsafe=False,
            is_microplastic=False,
            is_animal_derived=False,
            is_irritant=False,
            functions=[],
            warnings=["Unknown ingredient - proceed with caution"],
            description=f"Ingredient information not available for: {name}"
        )
    
    def analyze_all(self, ingredients_text: str) -> Dict[str, Any]:
        """Analyze all ingredients in a product."""
        ingredients = self.parse_ingredients(ingredients_text)
        
        analyzed = []
        warnings = []
        total_safety = 0
        ingredient_count = len(ingredients)
        
        for ing in ingredients:
            info = self.analyze_ingredient(ing)
            analyzed.append(info)
            total_safety += info.safety_score
            
            # Collect warnings
            if info.category == IngredientCategory.HAZARDOUS:
                warnings.append(f"⚠️ HAZARDOUS: {info.name} - {info.warnings[0] if info.warnings else 'Avoid this ingredient'}")
            if info.is_endocrine_disruptor:
                warnings.append(f"⚠️ ENDOCRINE DISRUPTOR: {info.name}")
            if info.is_pregnancy_unsafe:
                warnings.append(f"⚠️ PREGNANCY UNSAFE: {info.name}")
            if info.is_microplastic:
                warnings.append(f"⚠️ MICROPLASTIC: {info.name}")
            if info.is_irritant:
                warnings.append(f"⚠️ IRRITANT: {info.name}")
            if info.is_allergen:
                warnings.append(f"⚠️ ALLERGEN: {info.name}")
        
        # Calculate overall safety score
        overall_safety = total_safety / ingredient_count if ingredient_count > 0 else 0.5
        
        # Generate recommendations
        recommendations = []
        if any(i.is_comedogenic for i in analyzed):
            recommendations.append("Consider products with non-comedogenic ingredients")
        if any(i.is_fragrance for i in analyzed):
            recommendations.append("For sensitive skin, consider fragrance-free alternatives")
        if any(i.is_irritant for i in analyzed):
            recommendations.append("Patch test recommended before full application")
        if any(i.is_pregnancy_unsafe for i in analyzed):
            recommendations.append("Consult doctor if pregnant or planning pregnancy")
        
        return {
            "ingredients": analyzed,
            "safety_score": round(overall_safety, 2),
            "warnings": warnings,
            "recommendations": recommendations,
            "ingredient_count": ingredient_count,
            "hazardous_count": sum(1 for i in analyzed if i.category == IngredientCategory.HAZARDOUS),
            "safe_count": sum(1 for i in analyzed if i.category == IngredientCategory.SAFE),
            "moderate_count": sum(1 for i in analyzed if i.category == IngredientCategory.MODERATE),
            "unknown_count": sum(1 for i in analyzed if i.category == IngredientCategory.UNKNOWN),
        }
    
    def calculate_comedogenic_score(self, ingredients_text: str) -> float:
        """Calculate overall comedogenic score from ingredients."""
        ingredients = self.parse_ingredients(ingredients_text)
        
        total_score = 0
        count = 0
        
        for ing in ingredients:
            info = self.analyze_ingredient(ing)
            if info.comedogenic_rating > 0:
                total_score += info.comedogenic_rating
                count += 1
        
        return min(total_score / max(count, 1), 5.0)
    
    def calculate_fragrance_level(self, ingredients_text: str) -> float:
        """Calculate fragrance level from ingredients (0-1)."""
        ingredients = self.parse_ingredients(ingredients_text)
        
        fragrance_count = sum(1 for ing in ingredients if self.analyze_ingredient(ing).is_fragrance)
        return min(fragrance_count / max(len(ingredients), 1), 1.0)
    
    def calculate_alcohol_level(self, ingredients_text: str) -> float:
        """Calculate alcohol presence level from ingredients (0-1)."""
        ingredients = self.parse_ingredients(ingredients_text)
        
        alcohol_alcohols = ['alcohol denat', 'ethanol', 'isopropyl alcohol', 'sd alcohol']
        alcohol_count = sum(1 for ing in ingredients if any(a in ing.lower() for a in alcohol_alcohols))
        
        return min(alcohol_count / max(len(ingredients), 1), 1.0)


# Global analyzer instance
ingredient_analyzer = IngredientAnalyzer()
