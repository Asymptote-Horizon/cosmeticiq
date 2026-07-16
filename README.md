# CosmeticIQ

AI-Powered Cosmetic Safety & Suitability Platform using Fuzzy Logic, Soft Computing, and Scientific Ingredient Analysis.

## Architecture

```
CosmeticIQ/
├── backend/                   # FastAPI Python Backend
│   ├── app/
│   │   ├── api/v1/           # API Routes
│   │   ├── core/             # Configuration & Database
│   │   ├── models/           # SQLAlchemy Models
│   │   ├── schemas/          # Pydantic Schemas
│   │   ├── services/         # Business Logic
│   │   ├── decision_engine/  # Fuzzy Logic Engine
│   │   ├── ai/               # AI/ML Services
│   │   └── utils/            # Utilities & Seed Data
│   ├── tests/                # Test Suite
│   └── migrations/           # Alembic Migrations
│
├── frontend/                  # Next.js React Frontend
│   └── src/
│       ├── app/              # Pages (App Router)
│       ├── components/       # Reusable Components
│       └── lib/              # API Client & Store
│
├── .github/workflows/        # CI/CD Pipeline
├── docker-compose.yml        # Docker Orchestration
└── README.md
```

## Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11)
- **Database:** PostgreSQL + SQLAlchemy (Async)
- **Search:** Elasticsearch
- **Cache:** Redis
- **AI:** OpenAI / Gemini, Sentence Transformers
- **Decision Engine:** scikit-fuzzy (Fuzzy Logic)

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Animation:** Framer Motion
- **State:** Zustand
- **Charts:** Recharts

## Core Features

### 1. Fuzzy Logic Decision Engine
The PRIMARY decision maker uses 60+ fuzzy rules to evaluate product suitability based on:
- Skin Type (Dry, Oily, Sensitive, Acne-Prone)
- Age
- Climate (Humid, Dry, Cold)
- Budget
- Ingredient Safety
- Comedogenic Rating
- Fragrance Level
- Alcohol Presence
- Scientific Evidence
- Dermatologist Approval

**Important:** The LLM only EXPLAINS the fuzzy logic output - it never makes the recommendation directly.

### 2. AI Ingredient Analyzer
- Identifies safe, harmful, and unknown ingredients
- Detects allergens, endocrine disruptors, comedogenic ingredients
- Checks pregnancy safety
- Identifies microplastics and animal-derived ingredients
- Provides EWG scores and FDA status

### 3. Product Scanner
- Barcode scanning with OpenBeautyFacts integration
- Image upload with OCR extraction
- Text-based ingredient search

### 4. Influencer Truth Detector
- Verifies cosmetic claims against scientific literature
- Output: Supported, Partially Supported, Misleading, No Evidence

### 5. Product Comparator
- Side-by-side comparison with fuzzy suitability scoring

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis
- Elasticsearch (optional)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Docker Setup

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register new user |
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/products/` | GET | List products |
| `/api/v1/products/{id}` | GET | Get product |
| `/api/v1/products/search/{q}` | GET | Search products |
| `/api/v1/products/barcode/{bc}` | GET | Lookup by barcode |
| `/api/v1/products/scan` | POST | Scan product image |
| `/api/v1/ingredients/analyze` | POST | Analyze ingredients |
| `/api/v1/ingredients/search/{name}` | GET | Search ingredient |
| `/api/v1/recommendations/analyze` | POST | Get recommendation |
| `/api/v1/recommendations/compare` | POST | Compare products |
| `/api/v1/recommendations/fuzzy-evaluate` | POST | Test fuzzy engine |
| `/api/v1/claims/analyze` | POST | Verify influencer claim |
| `/api/v1/users/profile` | GET/PUT | User profile |
| `/api/v1/admin/stats` | GET | Admin statistics |

## Fuzzy Logic Rules

The engine uses 60+ rules across categories:

### Safety Rules
- IF skin sensitive AND fragrance high AND alcohol high THEN suitability = very_bad
- IF ingredient safety unsafe AND alcohol high THEN suitability = very_bad
- IF ingredient safety safe AND fragrance none AND alcohol none THEN suitability = excellent

### Skin Type Rules
- IF skin type oily AND comedogenic high THEN suitability = very_bad
- IF skin type acne AND comedogenic none AND fragrance none THEN suitability = excellent
- IF skin type dry AND climate dry AND ingredient safety safe THEN suitability = excellent

### Quality Rules
- IF product rating excellent AND scientific evidence strong AND dermatologist approval full THEN suitability = excellent
- IF budget high AND scientific evidence strong THEN suitability = excellent

See `backend/app/decision_engine/fuzzy_engine.py` for all rules.

## Testing

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_fuzzy_engine.py -v
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/cosmeticiq
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
ELASTICSEARCH_URL=http://localhost:9200
REDIS_URL=redis://localhost:6379/0
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Data Sources

- OpenBeautyFacts - Product database
- INCIDecoder - Ingredient information
- EWG Skin Deep - Safety scores
- PubMed - Scientific studies
- CosDNA - Ingredient analysis

## License

MIT License
