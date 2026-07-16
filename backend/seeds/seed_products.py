"""
Seed the products table from JSON data.
Usage: python -m seeds.seed_products
"""
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import async_session, init_db
from app.models.database_models import Product


async def seed_products():
    await init_db()

    json_path = os.path.join(os.path.dirname(__file__), "products_seed.json")
    with open(json_path, "r", encoding="utf-8") as f:
        products_data = json.load(f)

    async with async_session() as session:
        existing = await session.execute(
            __import__("sqlalchemy").select(__import__("sqlalchemy").func.count(Product.id))
        )
        count = existing.scalar()
        if count > 0:
            print(f"Database already has {count} products. Clearing...")
            await session.execute(__import__("sqlalchemy").text("DELETE FROM products"))
            await session.commit()

        created = 0
        for pd in products_data:
            product = Product(
                name=pd["name"],
                brand=pd["brand"],
                category=pd.get("category"),
                subcategory=pd.get("subcategory"),
                description=pd.get("description"),
                price=pd.get("price"),
                currency=pd.get("currency", "USD"),
                barcode=pd.get("barcode"),
                image_url=pd.get("image_url"),
                rating=pd.get("rating", 3.5),
                review_count=pd.get("review_count", 1000),
                is_vegan=pd.get("is_vegan", False),
                is_cruelty_free=pd.get("is_cruelty_free", False),
                is_organic=pd.get("is_organic", False),
                comedogenic_score=pd.get("comedogenic_score", 0),
                fragrance_level=pd.get("fragrance_level", 0),
                alcohol_level=pd.get("alcohol_level", 0),
                scientific_score=pd.get("scientific_score", 0.5),
                safety_score=pd.get("safety_score", 0.7),
                data_source=pd.get("data_source", "Manual"),
            )
            session.add(product)
            created += 1

        await session.commit()
        print(f"Successfully seeded {created} products!")


if __name__ == "__main__":
    asyncio.run(seed_products())
