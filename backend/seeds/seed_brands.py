"""
Seed the brands table from JSON data.
Usage: python -m seeds.seed_brands
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import async_session, init_db
from app.models.database_models import Brand


async def seed_brands():
    await init_db()

    json_path = os.path.join(os.path.dirname(__file__), "brands_seed.json")
    with open(json_path, "r", encoding="utf-8") as f:
        brands_data = json.load(f)

    async with async_session() as session:
        existing = await session.execute(
            __import__("sqlalchemy").select(__import__("sqlalchemy").func.count(Brand.id))
        )
        count = existing.scalar()
        if count > 0:
            print(f"Database already has {count} brands. Clearing...")
            await session.execute(__import__("sqlalchemy").text("DELETE FROM brands"))
            await session.commit()

        created = 0
        for bd in brands_data:
            brand = Brand(
                company_name=bd["company_name"],
                country=bd.get("country"),
                founded_year=bd.get("founded_year"),
                parent_company=bd.get("parent_company"),
                brand_type=bd.get("brand_type"),
                cruelty_free=bd.get("cruelty_free", False),
                vegan_products=bd.get("vegan_products", False),
                dermatologist_recommended=bd.get("dermatologist_recommended", False),
                official_website=bd.get("official_website"),
                logo_url=bd.get("logo_url"),
                description=bd.get("description"),
                popularity_score=bd.get("popularity_score", 0),
                sustainability_score=bd.get("sustainability_score", 0),
                average_price_range=bd.get("average_price_range"),
            )
            session.add(brand)
            created += 1

        await session.commit()
        print(f"Successfully seeded {created} brands!")


if __name__ == "__main__":
    asyncio.run(seed_brands())
