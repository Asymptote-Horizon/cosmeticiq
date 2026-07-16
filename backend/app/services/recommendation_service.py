from typing import Dict, List, Any, Optional
from app.decision_engine.fuzzy_engine import fuzzy_engine
from app.ai.ingredient_analyzer import ingredient_analyzer


class RecommendationService:
    """Personalized recommendation engine using fuzzy logic."""
    
    def __init__(self):
        self.fuzzy = fuzzy_engine
        self.analyzer = ingredient_analyzer
    
    def get_recommendation(self, product_data: Dict[str, Any], 
                          user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized recommendation for a product.
        
        Args:
            product_data: Product information including ingredients
            user_profile: User's skin profile and preferences
            
        Returns:
            Complete recommendation with fuzzy output and explanation
        """
        # Convert user profile to fuzzy inputs
        fuzzy_inputs = self._prepare_fuzzy_inputs(product_data, user_profile)
        
        # Run fuzzy logic engine
        fuzzy_output = self.fuzzy.evaluate(fuzzy_inputs)
        
        # Calculate additional metrics
        ingredient_analysis = self._analyze_ingredients(product_data.get('ingredients', ''))
        
        # Generate explanation
        explanation = self._generate_explanation(product_data, user_profile, fuzzy_output, ingredient_analysis)
        
        return {
            "product": product_data,
            "fuzzy_output": fuzzy_output,
            "explanation": explanation,
            "confidence_score": fuzzy_output.get('confidence', 0.5),
            "ingredients_analysis": ingredient_analysis,
            "triggered_rules": fuzzy_output.get('triggered_rules', []),
        }
    
    def _prepare_fuzzy_inputs(self, product_data: Dict[str, Any], 
                               user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Convert product and user data to fuzzy engine inputs."""
        
        # Skin type mapping
        skin_type = user_profile.get('skin_type', 'normal').lower()
        skin_type_map = {
            'dry': {'dry': 1.0, 'oily': 0.0, 'sensitive': 0.0, 'acne': 0.0},
            'oily': {'dry': 0.0, 'oily': 1.0, 'sensitive': 0.0, 'acne': 0.3},
            'combination': {'dry': 0.5, 'oily': 0.5, 'sensitive': 0.2, 'acne': 0.2},
            'sensitive': {'dry': 0.3, 'oily': 0.0, 'sensitive': 1.0, 'acne': 0.2},
            'acne prone': {'dry': 0.0, 'oily': 0.7, 'sensitive': 0.3, 'acne': 1.0},
            'normal': {'dry': 0.3, 'oily': 0.3, 'sensitive': 0.2, 'acne': 0.1},
        }
        
        skin_values = skin_type_map.get(skin_type, skin_type_map['normal'])
        
        # Climate mapping
        climate = user_profile.get('climate', 'moderate').lower()
        climate_map = {
            'humid': {'humid': 0.9, 'dry': 0.1, 'cold': 0.0},
            'dry': {'humid': 0.1, 'dry': 0.9, 'cold': 0.2},
            'cold': {'humid': 0.0, 'dry': 0.3, 'cold': 0.9},
            'tropical': {'humid': 0.9, 'dry': 0.0, 'cold': 0.0},
            'temperate': {'humid': 0.5, 'dry': 0.5, 'cold': 0.3},
            'moderate': {'humid': 0.5, 'dry': 0.5, 'cold': 0.5},
        }
        
        climate_values = climate_map.get(climate, climate_map['moderate'])
        
        # Product metrics
        ingredients_text = product_data.get('ingredients', '')
        ingredient_analysis = self.analyzer.analyze_all(ingredients_text)
        
        return {
            'skin_type_dry': skin_values['dry'],
            'skin_type_oily': skin_values['oily'],
            'skin_type_sensitive': skin_values['sensitive'],
            'skin_type_acne': skin_values['acne'],
            'age': user_profile.get('age', 30),
            'climate_humid': climate_values['humid'],
            'climate_dry': climate_values['dry'],
            'climate_cold': climate_values['cold'],
            'budget': user_profile.get('budget_max', 200),
            'ingredient_safety': ingredient_analysis.get('safety_score', 0.5),
            'comedogenic_rating': self.analyzer.calculate_comedogenic_score(ingredients_text),
            'fragrance_level': self.analyzer.calculate_fragrance_level(ingredients_text),
            'alcohol_presence': self.analyzer.calculate_alcohol_level(ingredients_text),
            'product_rating': product_data.get('rating', 3.0),
            'scientific_evidence': product_data.get('scientific_score', 0.5),
            'dermatologist_approval': product_data.get('dermatologist_approval', 0.5),
        }
    
    def _analyze_ingredients(self, ingredients_text: str) -> Dict[str, Any]:
        """Analyze ingredients for safety profile."""
        if not ingredients_text:
            return {
                'safe_count': 0,
                'moderate_count': 0,
                'hazardous_count': 0,
                'unknown_count': 0,
                'warnings': [],
                'score': 0.5
            }
        
        result = self.analyzer.analyze_all(ingredients_text)
        return result
    
    def _generate_explanation(self, product_data: Dict[str, Any], 
                               user_profile: Dict[str, Any],
                               fuzzy_output: Dict[str, Any],
                               ingredient_analysis: Dict[str, Any]) -> str:
        """Generate human-readable explanation."""
        
        score = fuzzy_output.get('suitability_score', 0.5)
        linguistic = fuzzy_output.get('linguistic_output', 'Average')
        
        # Start with fuzzy output
        explanation = f"## Product Suitability: {linguistic}\n\n"
        explanation += f"**Suitability Score:** {score:.1%}\n\n"
        
        # Add user context
        skin_type = user_profile.get('skin_type', 'normal')
        explanation += f"Based on your **{skin_type}** skin type, "
        
        # Add key factors
        triggered_rules = fuzzy_output.get('triggered_rules', [])
        if triggered_rules:
            explanation += "the following factors were considered:\n"
            for rule in triggered_rules[:3]:
                conditions = rule.get('conditions', {})
                condition_str = ", ".join([f"{k} is {v}" for k, v in conditions.items()])
                explanation += f"- {condition_str}\n"
        
        # Add ingredient insights
        if ingredient_analysis.get('safe_count', 0) > 0:
            explanation += f"\n**Good news:** {ingredient_analysis['safe_count']} safe ingredients found.\n"
        
        if ingredient_analysis.get('hazardous_count', 0) > 0:
            explanation += f"\n**Caution:** {ingredient_analysis['hazardous_count']} potentially harmful ingredients detected.\n"
        
        # Add specific warnings
        warnings = ingredient_analysis.get('warnings', [])
        if warnings:
            explanation += "\n**Important warnings:**\n"
            for warning in warnings[:3]:
                explanation += f"- {warning}\n"
        
        # Final recommendation
        if score >= 0.7:
            explanation += "\n**Recommendation:** This product is suitable for you. Consider adding it to your routine."
        elif score >= 0.4:
            explanation += "\n**Recommendation:** This product may work for you, but monitor how your skin responds."
        else:
            explanation += "\n**Recommendation:** This product may not be ideal for your needs. Consider alternatives."
        
        return explanation
    
    def compare_products(self, products: List[Dict[str, Any]], 
                         user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Compare multiple products for a user."""
        recommendations = []
        
        for product in products:
            rec = self.get_recommendation(product, user_profile)
            recommendations.append(rec)
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x['fuzzy_output']['suitability_score'], reverse=True)
        
        # Generate comparison summary
        comparison = {
            "products": recommendations,
            "best_match": recommendations[0] if recommendations else None,
            "worst_match": recommendations[-1] if recommendations else None,
            "average_score": sum(r['fuzzy_output']['suitability_score'] for r in recommendations) / len(recommendations) if recommendations else 0,
            "recommendation": self._generate_comparison_recommendation(recommendations)
        }
        
        return comparison
    
    def _generate_comparison_recommendation(self, recommendations: List[Dict[str, Any]]) -> str:
        """Generate recommendation summary from comparison."""
        if not recommendations:
            return "No products to compare."
        
        best = recommendations[0]
        best_name = best['product'].get('name', 'Unknown')
        best_score = best['fuzzy_output']['suitability_score']
        best_linguistic = best['fuzzy_output']['linguistic_output']
        
        if best_score >= 0.7:
            return f"**{best_name}** is the best choice with a {best_linguistic} rating ({best_score:.0%}). It matches your profile well."
        elif best_score >= 0.5:
            return f"**{best_name}** is the most suitable option ({best_linguistic}, {best_score:.0%}), but consider your specific needs."
        else:
            return f"None of the compared products are highly suitable. Consider looking for alternatives."


# Global recommendation service
recommendation_service = RecommendationService()
