import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Dict, List, Any, Tuple
import json


class FuzzyCosmeticEngine:
    """
    Fuzzy Logic Decision Engine for Cosmetic Product Suitability.
    This is the PRIMARY decision maker - not the LLM.
    """
    
    def __init__(self):
        self.universes = {}
        self.rules = []
        self.control_system = None
        self.simulation = None
        self._initialize_variables()
        self._initialize_rules()
        self._build_control_system()
    
    def _initialize_variables(self):
        """Initialize all fuzzy variables with membership functions."""
        
        # Input Variables
        self.skin_type_dry = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'skin_type_dry')
        self.skin_type_oily = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'skin_type_oily')
        self.skin_type_sensitive = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'skin_type_sensitive')
        self.skin_type_acne = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'skin_type_acne')
        
        self.age = ctrl.Antecedent(np.arange(15, 80, 1), 'age')
        self.climate_humid = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'climate_humid')
        self.climate_dry = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'climate_dry')
        self.climate_cold = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'climate_cold')
        
        self.budget = ctrl.Antecedent(np.arange(0, 1001, 10), 'budget')
        self.ingredient_safety = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'ingredient_safety')
        self.comedogenic_rating = ctrl.Antecedent(np.arange(0, 5.1, 0.5), 'comedogenic_rating')
        self.fragrance_level = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'fragrance_level')
        self.alcohol_presence = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'alcohol_presence')
        self.product_rating = ctrl.Antecedent(np.arange(0, 5.1, 0.5), 'product_rating')
        self.scientific_evidence = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'scientific_evidence')
        self.dermatologist_approval = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'dermatologist_approval')
        
        # Output Variable
        self.suitability = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'suitability')
        
        # Skin Type Dry Membership Functions
        self.skin_type_dry['low'] = fuzz.trimf(self.skin_type_dry.universe, [0, 0, 0.5])
        self.skin_type_dry['medium'] = fuzz.trimf(self.skin_type_dry.universe, [0.2, 0.5, 0.8])
        self.skin_type_dry['high'] = fuzz.trimf(self.skin_type_dry.universe, [0.5, 1, 1])
        
        # Skin Type Oily Membership Functions
        self.skin_type_oily['low'] = fuzz.trimf(self.skin_type_oily.universe, [0, 0, 0.5])
        self.skin_type_oily['medium'] = fuzz.trimf(self.skin_type_oily.universe, [0.2, 0.5, 0.8])
        self.skin_type_oily['high'] = fuzz.trimf(self.skin_type_oily.universe, [0.5, 1, 1])
        
        # Skin Type Sensitive Membership Functions
        self.skin_type_sensitive['low'] = fuzz.trimf(self.skin_type_sensitive.universe, [0, 0, 0.5])
        self.skin_type_sensitive['medium'] = fuzz.trimf(self.skin_type_sensitive.universe, [0.2, 0.5, 0.8])
        self.skin_type_sensitive['high'] = fuzz.trimf(self.skin_type_sensitive.universe, [0.5, 1, 1])
        
        # Skin Type Acne Membership Functions
        self.skin_type_acne['low'] = fuzz.trimf(self.skin_type_acne.universe, [0, 0, 0.5])
        self.skin_type_acne['medium'] = fuzz.trimf(self.skin_type_acne.universe, [0.2, 0.5, 0.8])
        self.skin_type_acne['high'] = fuzz.trimf(self.skin_type_acne.universe, [0.5, 1, 1])
        
        # Age Membership Functions
        self.age['young'] = fuzz.trimf(self.age.universe, [15, 15, 30])
        self.age['mature'] = fuzz.trimf(self.age.universe, [25, 40, 55])
        self.age['senior'] = fuzz.trimf(self.age.universe, [50, 80, 80])
        
        # Climate Humid Membership Functions
        self.climate_humid['low'] = fuzz.trimf(self.climate_humid.universe, [0, 0, 0.5])
        self.climate_humid['medium'] = fuzz.trimf(self.climate_humid.universe, [0.2, 0.5, 0.8])
        self.climate_humid['high'] = fuzz.trimf(self.climate_humid.universe, [0.5, 1, 1])
        
        # Climate Dry Membership Functions
        self.climate_dry['low'] = fuzz.trimf(self.climate_dry.universe, [0, 0, 0.5])
        self.climate_dry['medium'] = fuzz.trimf(self.climate_dry.universe, [0.2, 0.5, 0.8])
        self.climate_dry['high'] = fuzz.trimf(self.climate_dry.universe, [0.5, 1, 1])
        
        # Climate Cold Membership Functions
        self.climate_cold['low'] = fuzz.trimf(self.climate_cold.universe, [0, 0, 0.5])
        self.climate_cold['medium'] = fuzz.trimf(self.climate_cold.universe, [0.2, 0.5, 0.8])
        self.climate_cold['high'] = fuzz.trimf(self.climate_cold.universe, [0.5, 1, 1])
        
        # Budget Membership Functions
        self.budget['low'] = fuzz.trimf(self.budget.universe, [0, 0, 200])
        self.budget['medium'] = fuzz.trimf(self.budget.universe, [100, 400, 600])
        self.budget['high'] = fuzz.trimf(self.budget.universe, [500, 1000, 1000])
        
        # Ingredient Safety Membership Functions
        self.ingredient_safety['unsafe'] = fuzz.trimf(self.ingredient_safety.universe, [0, 0, 0.4])
        self.ingredient_safety['moderate'] = fuzz.trimf(self.ingredient_safety.universe, [0.3, 0.5, 0.7])
        self.ingredient_safety['safe'] = fuzz.trimf(self.ingredient_safety.universe, [0.6, 1, 1])
        
        # Comedogenic Rating Membership Functions
        self.comedogenic_rating['none'] = fuzz.trimf(self.comedogenic_rating.universe, [0, 0, 1])
        self.comedogenic_rating['low'] = fuzz.trimf(self.comedogenic_rating.universe, [0.5, 1.5, 2])
        self.comedogenic_rating['moderate'] = fuzz.trimf(self.comedogenic_rating.universe, [1.5, 2.5, 3.5])
        self.comedogenic_rating['high'] = fuzz.trimf(self.comedogenic_rating.universe, [3, 4, 5])
        
        # Fragrance Level Membership Functions
        self.fragrance_level['none'] = fuzz.trimf(self.fragrance_level.universe, [0, 0, 0.2])
        self.fragrance_level['low'] = fuzz.trimf(self.fragrance_level.universe, [0.1, 0.3, 0.5])
        self.fragrance_level['moderate'] = fuzz.trimf(self.fragrance_level.universe, [0.4, 0.6, 0.8])
        self.fragrance_level['high'] = fuzz.trimf(self.fragrance_level.universe, [0.7, 1, 1])
        
        # Alcohol Presence Membership Functions
        self.alcohol_presence['none'] = fuzz.trimf(self.alcohol_presence.universe, [0, 0, 0.2])
        self.alcohol_presence['low'] = fuzz.trimf(self.alcohol_presence.universe, [0.1, 0.3, 0.5])
        self.alcohol_presence['moderate'] = fuzz.trimf(self.alcohol_presence.universe, [0.4, 0.6, 0.8])
        self.alcohol_presence['high'] = fuzz.trimf(self.alcohol_presence.universe, [0.7, 1, 1])
        
        # Product Rating Membership Functions
        self.product_rating['poor'] = fuzz.trimf(self.product_rating.universe, [0, 0, 2])
        self.product_rating['average'] = fuzz.trimf(self.product_rating.universe, [1.5, 2.5, 3.5])
        self.product_rating['good'] = fuzz.trimf(self.product_rating.universe, [3, 4, 5])
        self.product_rating['excellent'] = fuzz.trimf(self.product_rating.universe, [4, 5, 5])
        
        # Scientific Evidence Membership Functions
        self.scientific_evidence['weak'] = fuzz.trimf(self.scientific_evidence.universe, [0, 0, 0.4])
        self.scientific_evidence['moderate'] = fuzz.trimf(self.scientific_evidence.universe, [0.3, 0.5, 0.7])
        self.scientific_evidence['strong'] = fuzz.trimf(self.scientific_evidence.universe, [0.6, 1, 1])
        
        # Dermatologist Approval Membership Functions
        self.dermatologist_approval['none'] = fuzz.trimf(self.dermatologist_approval.universe, [0, 0, 0.3])
        self.dermatologist_approval['partial'] = fuzz.trimf(self.dermatologist_approval.universe, [0.2, 0.5, 0.8])
        self.dermatologist_approval['full'] = fuzz.trimf(self.dermatologist_approval.universe, [0.7, 1, 1])
        
        # Output Suitability Membership Functions
        self.suitability['very_bad'] = fuzz.trimf(self.suitability.universe, [0, 0, 0.2])
        self.suitability['bad'] = fuzz.trimf(self.suitability.universe, [0.1, 0.3, 0.5])
        self.suitability['average'] = fuzz.trimf(self.suitability.universe, [0.3, 0.5, 0.7])
        self.suitability['good'] = fuzz.trimf(self.suitability.universe, [0.5, 0.7, 0.9])
        self.suitability['excellent'] = fuzz.trimf(self.suitability.universe, [0.8, 1, 1])
    
    def _initialize_rules(self):
        """Initialize 50+ fuzzy rules for cosmetic suitability."""
        
        # Rule 1-5: Sensitive Skin Rules
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['high'] & self.fragrance_level['high'] & self.alcohol_presence['high'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['high'] & self.fragrance_level['low'] & self.alcohol_presence['low'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['high'] & self.ingredient_safety['safe'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['high'] & self.ingredient_safety['unsafe'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['medium'] & self.fragrance_level['moderate'] & self.alcohol_presence['moderate'],
            self.suitability['average']
        ))
        
        # Rule 6-10: Dry Skin Rules
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['high'] & self.climate_dry['high'] & self.ingredient_safety['safe'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['high'] & self.climate_cold['high'] & self.alcohol_presence['high'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['high'] & self.fragrance_level['none'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['medium'] & self.climate_humid['medium'],
            self.suitability['average']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['high'] & self.ingredient_safety['safe'] & self.scientific_evidence['strong'],
            self.suitability['excellent']
        ))
        
        # Rule 11-15: Oily Skin Rules
        self.rules.append(ctrl.Rule(
            self.skin_type_oily['high'] & self.comedogenic_rating['high'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_oily['high'] & self.comedogenic_rating['none'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_oily['medium'] & self.climate_humid['high'] & self.fragrance_level['high'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_oily['high'] & self.alcohol_presence['low'] & self.ingredient_safety['safe'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_oily['medium'] & self.comedogenic_rating['low'],
            self.suitability['average']
        ))
        
        # Rule 16-20: Acne-Prone Skin Rules
        self.rules.append(ctrl.Rule(
            self.skin_type_acne['high'] & self.comedogenic_rating['high'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_acne['high'] & self.comedogenic_rating['none'] & self.fragrance_level['none'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_acne['high'] & self.fragrance_level['high'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_acne['medium'] & self.ingredient_safety['safe'] & self.dermatologist_approval['full'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_acne['high'] & self.alcohol_presence['moderate'],
            self.suitability['average']
        ))
        
        # Rule 21-25: Age-Based Rules
        self.rules.append(ctrl.Rule(
            self.age['young'] & self.fragrance_level['high'] & self.skin_type_sensitive['high'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.age['mature'] & self.scientific_evidence['strong'] & self.ingredient_safety['safe'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.age['senior'] & self.dermatologist_approval['full'] & self.fragrance_level['low'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.age['young'] & self.comedogenic_rating['none'] & self.ingredient_safety['safe'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.age['senior'] & self.alcohol_presence['high'],
            self.suitability['bad']
        ))
        
        # Rule 26-30: Climate-Based Rules
        self.rules.append(ctrl.Rule(
            self.climate_humid['high'] & self.skin_type_oily['high'] & self.fragrance_level['high'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.climate_dry['high'] & self.skin_type_dry['high'] & self.ingredient_safety['safe'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.climate_cold['high'] & self.alcohol_presence['high'] & self.skin_type_sensitive['high'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.climate_humid['medium'] & self.comedogenic_rating['low'],
            self.suitability['average']
        ))
        
        self.rules.append(ctrl.Rule(
            self.climate_dry['high'] & self.fragrance_level['none'] & self.ingredient_safety['safe'],
            self.suitability['excellent']
        ))
        
        # Rule 31-35: Budget-Based Rules
        self.rules.append(ctrl.Rule(
            self.budget['low'] & self.ingredient_safety['safe'] & self.product_rating['good'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.budget['high'] & self.scientific_evidence['strong'] & self.dermatologist_approval['full'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.budget['medium'] & self.ingredient_safety['moderate'],
            self.suitability['average']
        ))
        
        self.rules.append(ctrl.Rule(
            self.budget['low'] & self.ingredient_safety['unsafe'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.budget['high'] & self.product_rating['excellent'] & self.scientific_evidence['strong'],
            self.suitability['excellent']
        ))
        
        # Rule 36-40: Product Quality Rules
        self.rules.append(ctrl.Rule(
            self.product_rating['excellent'] & self.scientific_evidence['strong'] & self.dermatologist_approval['full'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.product_rating['poor'] & self.ingredient_safety['unsafe'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.product_rating['good'] & self.ingredient_safety['safe'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.scientific_evidence['strong'] & self.dermatologist_approval['full'] & self.fragrance_level['low'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.product_rating['average'] & self.ingredient_safety['moderate'],
            self.suitability['average']
        ))
        
        # Rule 41-45: Safety-Critical Rules
        self.rules.append(ctrl.Rule(
            self.ingredient_safety['unsafe'] & self.fragrance_level['high'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.ingredient_safety['unsafe'] & self.alcohol_presence['high'],
            self.suitability['very_bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.ingredient_safety['safe'] & self.fragrance_level['none'] & self.alcohol_presence['none'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.ingredient_safety['moderate'] & self.comedogenic_rating['moderate'],
            self.suitability['average']
        ))
        
        self.rules.append(ctrl.Rule(
            self.ingredient_safety['safe'] & self.scientific_evidence['moderate'] & self.product_rating['good'],
            self.suitability['good']
        ))
        
        # Rule 46-50: Complex Combination Rules
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['high'] & self.skin_type_acne['high'] & self.fragrance_level['none'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['high'] & self.skin_type_sensitive['medium'] & self.alcohol_presence['low'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_oily['high'] & self.skin_type_acne['medium'] & self.comedogenic_rating['low'],
            self.suitability['average']
        ))
        
        self.rules.append(ctrl.Rule(
            self.age['mature'] & self.skin_type_dry['medium'] & self.scientific_evidence['strong'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.climate_cold['high'] & self.skin_type_sensitive['high'] & self.ingredient_safety['safe'],
            self.suitability['good']
        ))
        
        # Rule 51-55: Advanced Combination Rules
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['high'] & self.climate_cold['high'] & self.fragrance_level['none'] & self.alcohol_presence['none'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_oily['high'] & self.climate_humid['high'] & self.comedogenic_rating['none'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_acne['high'] & self.fragrance_level['low'] & self.alcohol_presence['low'] & self.dermatologist_approval['full'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.age['young'] & self.skin_type_oily['medium'] & self.budget['low'] & self.ingredient_safety['safe'],
            self.suitability['good']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['high'] & self.age['senior'] & self.scientific_evidence['strong'] & self.fragrance_level['low'],
            self.suitability['excellent']
        ))
        
        # Rule 56-60: Edge Case Rules
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['medium'] & self.alcohol_presence['high'] & self.fragrance_level['high'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.comedogenic_rating['high'] & self.scientific_evidence['weak'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.dermatologist_approval['none'] & self.ingredient_safety['moderate'] & self.fragrance_level['high'],
            self.suitability['bad']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_dry['medium'] & self.budget['high'] & self.ingredient_safety['safe'] & self.scientific_evidence['strong'],
            self.suitability['excellent']
        ))
        
        self.rules.append(ctrl.Rule(
            self.skin_type_sensitive['high'] & self.budget['medium'] & self.ingredient_safety['safe'] & self.fragrance_level['low'],
            self.suitability['good']
        ))
    
    def _build_control_system(self):
        """Build the fuzzy control system from rules."""
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)
    
    def evaluate(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate product suitability using fuzzy logic.
        
        Args:
            inputs: Dictionary containing all input variables
            
        Returns:
            Dictionary with fuzzy output and metadata
        """
        try:
            # Set input values
            self.simulation.input['skin_type_dry'] = inputs.get('skin_type_dry', 0)
            self.simulation.input['skin_type_oily'] = inputs.get('skin_type_oily', 0)
            self.simulation.input['skin_type_sensitive'] = inputs.get('skin_type_sensitive', 0)
            self.simulation.input['skin_type_acne'] = inputs.get('skin_type_acne', 0)
            self.simulation.input['age'] = inputs.get('age', 30)
            self.simulation.input['climate_humid'] = inputs.get('climate_humid', 0)
            self.simulation.input['climate_dry'] = inputs.get('climate_dry', 0)
            self.simulation.input['climate_cold'] = inputs.get('climate_cold', 0)
            self.simulation.input['budget'] = inputs.get('budget', 200)
            self.simulation.input['ingredient_safety'] = inputs.get('ingredient_safety', 0.5)
            self.simulation.input['comedogenic_rating'] = inputs.get('comedogenic_rating', 0)
            self.simulation.input['fragrance_level'] = inputs.get('fragrance_level', 0)
            self.simulation.input['alcohol_presence'] = inputs.get('alcohol_presence', 0)
            self.simulation.input['product_rating'] = inputs.get('product_rating', 3)
            self.simulation.input['scientific_evidence'] = inputs.get('scientific_evidence', 0.5)
            self.simulation.input['dermatologist_approval'] = inputs.get('dermatologist_approval', 0.5)
            
            # Compute
            self.simulation.compute()
            
            # Get output
            suitability_score = self.simulation.output['suitability']
            
            # Determine linguistic output
            if suitability_score <= 0.2:
                linguistic_output = "Very Bad"
            elif suitability_score <= 0.4:
                linguistic_output = "Bad"
            elif suitability_score <= 0.6:
                linguistic_output = "Average"
            elif suitability_score <= 0.8:
                linguistic_output = "Good"
            else:
                linguistic_output = "Excellent"
            
            # Calculate membership values
            membership_values = {
                'very_bad': fuzz.interp_membership(self.suitability.universe, self.suitability['very_bad'].mf, suitability_score),
                'bad': fuzz.interp_membership(self.suitability.universe, self.suitability['bad'].mf, suitability_score),
                'average': fuzz.interp_membership(self.suitability.universe, self.suitability['average'].mf, suitability_score),
                'good': fuzz.interp_membership(self.suitability.universe, self.suitability['good'].mf, suitability_score),
                'excellent': fuzz.interp_membership(self.suitability.universe, self.suitability['excellent'].mf, suitability_score),
            }
            
            # Find triggered rules
            triggered_rules = self._find_triggered_rules(inputs)
            
            return {
                'suitability_score': round(suitability_score, 4),
                'confidence': round(max(membership_values.values()), 4),
                'linguistic_output': linguistic_output,
                'membership_values': membership_values,
                'triggered_rules': triggered_rules
            }
            
        except Exception as e:
            return {
                'suitability_score': 0.5,
                'confidence': 0.0,
                'linguistic_output': 'Average',
                'membership_values': {},
                'triggered_rules': [],
                'error': str(e)
            }
    
    def _find_triggered_rules(self, inputs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find which rules were triggered by the inputs."""
        triggered = []
        
        for rule in self.rules:
            try:
                # Check if rule conditions are met
                antecedent_values = []
                for antecedent in rule.antecedent:
                    input_key = antecedent.var_name
                    term_name = antecedent.term_name
                    if input_key in inputs:
                        # Simple threshold check
                        if term_name == 'high' and inputs[input_key] >= 0.7:
                            antecedent_values.append(True)
                        elif term_name == 'medium' and 0.3 <= inputs[input_key] <= 0.7:
                            antecedent_values.append(True)
                        elif term_name == 'low' and inputs[input_key] <= 0.3:
                            antecedent_values.append(True)
                        else:
                            antecedent_values.append(False)
                    else:
                        antecedent_values.append(False)
                
                if all(antecedent_values):
                    triggered.append({
                        'rule_id': len(triggered) + 1,
                        'conditions': {str(a.var_name): str(a.term_name) for a in rule.antecedent},
                        'output': str(rule.consequent.term_name),
                        'weight': 1.0
                    })
            except:
                continue
        
        return triggered[:10]  # Return top 10 triggered rules


# Global engine instance
fuzzy_engine = FuzzyCosmeticEngine()
