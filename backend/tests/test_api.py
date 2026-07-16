import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root():
    """Test root endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "CosmeticIQ"


@pytest.mark.asyncio
async def test_health():
    """Test health endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_register():
    """Test user registration."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_login():
    """Test user login."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # First register
        await client.post("/api/v1/auth/register", json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "testpassword123"
        })
        
        # Then login
        response = await client.post("/api/v1/auth/login", data={
            "username": "loginuser",
            "password": "testpassword123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_ingredient_analysis():
    """Test ingredient analysis endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/ingredients/analyze", json={
            "ingredients_text": "Water, Glycerin, Hyaluronic Acid, Niacinamide"
        })
        assert response.status_code == 200
        data = response.json()
        assert "ingredients" in data
        assert "safety_score" in data


@pytest.mark.asyncio
async def test_ingredient_search():
    """Test ingredient search endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/api/v1/ingredients/search/hyaluronic%20acid")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Hyaluronic Acid"


@pytest.mark.asyncio
async def test_fuzzy_evaluate():
    """Test fuzzy logic evaluation endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/v1/recommendations/fuzzy-evaluate", json={
            "skin_type": "sensitive",
            "age": 30,
            "climate": "moderate",
            "budget": 200,
            "ingredient_safety": 0.7,
            "comedogenic_rating": 0,
            "fragrance_level": 0.8,
            "alcohol_presence": 0.7,
            "product_rating": 3.0,
            "scientific_evidence": 0.5,
            "dermatologist_approval": 0.5
        })
        assert response.status_code == 200
        data = response.json()
        assert "suitability_score" in data
        assert "linguistic_output" in data
