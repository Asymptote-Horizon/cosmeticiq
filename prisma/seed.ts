import { PrismaClient } from '@prisma/client';
import brands from '../backend/seeds/brands_seed.json';

const prisma = new PrismaClient();

interface BrandData {
  company_name: string;
  country: string | null;
  founded_year: number | null;
  parent_company: string | null;
  brand_type: string | null;
  cruelty_free: boolean;
  vegan_products: boolean;
  dermatologist_recommended: boolean;
  official_website: string | null;
  logo_url: string | null;
  description: string | null;
  popularity_score: number;
  sustainability_score: number;
  average_price_range: string | null;
}

async function main(): Promise<void> {
  console.log(`Starting seed with ${brands.length} brands...`);

  let created = 0;
  let updated = 0;
  const errors: string[] = [];

  for (const brand of brands as BrandData[]) {
    try {
      const result = await prisma.brand.upsert({
        where: { company_name: brand.company_name },
        update: {
          country: brand.country,
          founded_year: brand.founded_year,
          parent_company: brand.parent_company,
          brand_type: brand.brand_type,
          cruelty_free: brand.cruelty_free,
          vegan_products: brand.vegan_products,
          dermatologist_recommended: brand.dermatologist_recommended,
          official_website: brand.official_website,
          logo_url: brand.logo_url,
          description: brand.description,
          popularity_score: brand.popularity_score,
          sustainability_score: brand.sustainability_score,
          average_price_range: brand.average_price_range,
        },
        create: {
          company_name: brand.company_name,
          country: brand.country,
          founded_year: brand.founded_year,
          parent_company: brand.parent_company,
          brand_type: brand.brand_type,
          cruelty_free: brand.cruelty_free,
          vegan_products: brand.vegan_products,
          dermatologist_recommended: brand.dermatologist_recommended,
          official_website: brand.official_website,
          logo_url: brand.logo_url,
          description: brand.description,
          popularity_score: brand.popularity_score,
          sustainability_score: brand.sustainability_score,
          average_price_range: brand.average_price_range,
        },
      });

      if (result) {
        created++;
      } else {
        updated++;
      }

      console.log(`Processed: ${brand.company_name}`);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      errors.push(`${brand.company_name}: ${message}`);
      console.error(`Error processing ${brand.company_name}:`, message);
    }
  }

  console.log('\n--- Seed Summary ---');
  console.log(`Total brands processed: ${created + updated}`);
  console.log(`Created/Updated: ${created}`);
  console.log(`Skipped: ${updated}`);

  if (errors.length > 0) {
    console.log(`\nErrors (${errors.length}):`);
    errors.forEach((e) => console.log(`  - ${e}`));
  }

  console.log('Seed completed successfully!');
}

main()
  .catch((e) => {
    console.error('Fatal error during seeding:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
