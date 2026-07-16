import pytest
from app.ai.ingredient_analyzer import IngredientAnalyzer, IngredientCategory


@pytest.fixture
def analyzer():
    return IngredientAnalyzer()


def test_parse_ingredients_comma(analyzer):
    """Test parsing comma-separated ingredients."""
    text = "Water, Glycerin, Hyaluronic Acid, Niacinamide"
    result = analyzer.parse_ingredients(text)
    assert len(result) == 4
    assert 'water' in result
    assert 'glycerin' in result


def test_parse_ingredients_newline(analyzer):
    """Test parsing newline-separated ingredients."""
    text = "Water\nGlycerin\nHyaluronic Acid"
    result = analyzer.parse_ingredients(text)
    assert len(result) == 3


def test_analyze_known_ingredient(analyzer):
    """Test analyzing a known ingredient."""
    info = analyzer.analyze_ingredient("hyaluronic acid")
    assert info.name == "Hyaluronic Acid"
    assert info.category == IngredientCategory.SAFE
    assert info.safety_score >= 0.9


def test_analyze_hazardous_ingredient(analyzer):
    """Test analyzing a hazardous ingredient."""
    info = analyzer.analyze_ingredient("paraben")
    assert info.category == IngredientCategory.HAZARDOUS
    assert info.is_endocrine_disruptor is True
    assert info.safety_score < 0.5


def test_analyze_unknown_ingredient(analyzer):
    """Test analyzing an unknown ingredient."""
    info = analyzer.analyze_ingredient("xyz_unknown_ingredient")
    assert info.category == IngredientCategory.UNKNOWN


def test_analyze_all(analyzer):
    """Test analyzing multiple ingredients."""
    text = "Water, Glycerin, Hyaluronic Acid, Paraben, Fragrance"
    result = analyzer.analyze_all(text)
    
    assert result['ingredient_count'] == 5
    assert result['safe_count'] >= 2
    assert result['hazardous_count'] >= 1
    assert len(result['warnings']) > 0


def test_comedogenic_score(analyzer):
    """Test comedogenic score calculation."""
    text = "Water, Glycerin, Coconut Oil"
    score = analyzer.calculate_comedogenic_score(text)
    assert 0 <= score <= 5


def test_fragrance_level(analyzer):
    """Test fragrance level calculation."""
    # With fragrance
    text1 = "Water, Parfum, Fragrance"
    level1 = analyzer.calculate_fragrance_level(text1)
    assert level1 > 0
    
    # Without fragrance
    text2 = "Water, Glycerin, Hyaluronic Acid"
    level2 = analyzer.calculate_fragrance_level(text2)
    assert level2 == 0


def test_alcohol_level(analyzer):
    """Test alcohol level calculation."""
    # With alcohol
    text1 = "Water, Alcohol Denat, Glycerin"
    level1 = analyzer.calculate_alcohol_level(text1)
    assert level1 > 0
    
    # Without alcohol
    text2 = "Water, Glycerin"
    level2 = analyzer.calculate_alcohol_level(text2)
    assert level2 == 0
