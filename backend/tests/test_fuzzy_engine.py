import pytest
from app.decision_engine.fuzzy_engine import FuzzyCosmeticEngine


@pytest.fixture
def engine():
    return FuzzyCosmeticEngine()


def test_engine_initialization(engine):
    """Test that fuzzy engine initializes correctly."""
    assert engine.control_system is not None
    assert engine.simulation is not None
    assert len(engine.rules) >= 50


def test_basic_evaluation(engine):
    """Test basic fuzzy evaluation with default inputs."""
    inputs = {
        'skin_type_dry': 0.5,
        'skin_type_oily': 0.3,
        'skin_type_sensitive': 0.2,
        'skin_type_acne': 0.1,
        'age': 30,
        'climate_humid': 0.5,
        'climate_dry': 0.5,
        'climate_cold': 0.3,
        'budget': 200,
        'ingredient_safety': 0.7,
        'comedogenic_rating': 1,
        'fragrance_level': 0.2,
        'alcohol_presence': 0.1,
        'product_rating': 3.5,
        'scientific_evidence': 0.7,
        'dermatologist_approval': 0.6,
    }
    
    result = engine.evaluate(inputs)
    
    assert 'suitability_score' in result
    assert 'confidence' in result
    assert 'linguistic_output' in result
    assert 'membership_values' in result
    assert 0 <= result['suitability_score'] <= 1
    assert result['linguistic_output'] in ['Very Bad', 'Bad', 'Average', 'Good', 'Excellent']


def test_sensitive_skin_high_fragrance(engine):
    """Test that sensitive skin + high fragrance gives low score."""
    inputs = {
        'skin_type_dry': 0.0,
        'skin_type_oily': 0.0,
        'skin_type_sensitive': 1.0,
        'skin_type_acne': 0.0,
        'age': 30,
        'climate_humid': 0.5,
        'climate_dry': 0.5,
        'climate_cold': 0.5,
        'budget': 200,
        'ingredient_safety': 0.5,
        'comedogenic_rating': 0,
        'fragrance_level': 0.9,
        'alcohol_presence': 0.8,
        'product_rating': 3.0,
        'scientific_evidence': 0.5,
        'dermatologist_approval': 0.5,
    }
    
    result = engine.evaluate(inputs)
    
    # Should be low score due to sensitive skin + high fragrance + high alcohol
    assert result['suitability_score'] < 0.4


def test_safe_ingredients_good_score(engine):
    """Test that safe ingredients with good conditions give high score."""
    inputs = {
        'skin_type_dry': 0.3,
        'skin_type_oily': 0.3,
        'skin_type_sensitive': 0.2,
        'skin_type_acne': 0.1,
        'age': 35,
        'climate_humid': 0.5,
        'climate_dry': 0.5,
        'climate_cold': 0.3,
        'budget': 300,
        'ingredient_safety': 0.9,
        'comedogenic_rating': 0,
        'fragrance_level': 0.0,
        'alcohol_presence': 0.0,
        'product_rating': 4.5,
        'scientific_evidence': 0.9,
        'dermatologist_approval': 0.9,
    }
    
    result = engine.evaluate(inputs)
    
    # Should be high score
    assert result['suitability_score'] > 0.6


def test_acne_prone_high_comedogenic(engine):
    """Test that acne-prone skin + high comedogenic gives low score."""
    inputs = {
        'skin_type_dry': 0.0,
        'skin_type_oily': 0.7,
        'skin_type_sensitive': 0.3,
        'skin_type_acne': 1.0,
        'age': 25,
        'climate_humid': 0.5,
        'climate_dry': 0.5,
        'climate_cold': 0.3,
        'budget': 150,
        'ingredient_safety': 0.6,
        'comedogenic_rating': 4.0,
        'fragrance_level': 0.5,
        'alcohol_presence': 0.3,
        'product_rating': 3.0,
        'scientific_evidence': 0.5,
        'dermatologist_approval': 0.5,
    }
    
    result = engine.evaluate(inputs)
    
    # Should be low score
    assert result['suitability_score'] < 0.4
