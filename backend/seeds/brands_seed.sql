-- ============================================================
-- Cosmetic Brands Database Seed File
-- Contains 120+ cosmetic brands across multiple categories
-- Categories: Indian, Drugstore, Premium, Luxury, K-Beauty,
--             Clinical/Dermatologist, Organic, Additional
-- ============================================================

CREATE TABLE IF NOT EXISTS brands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100),
    founded_year INTEGER,
    parent_company VARCHAR(255),
    brand_type VARCHAR(100),
    cruelty_free BOOLEAN DEFAULT 0,
    vegan_products BOOLEAN DEFAULT 0,
    dermatologist_recommended BOOLEAN DEFAULT 0,
    official_website VARCHAR(500),
    logo_url VARCHAR(1000),
    description TEXT,
    popularity_score REAL DEFAULT 0,
    sustainability_score REAL DEFAULT 0,
    average_price_range VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELETE FROM brands;

-- ============================================================
-- INDIAN BRANDS (20)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Minimalist', 'India', 2020, NULL, 'Indian Brand', 1, 1, 1, 'https://www.minimalist.com', 'https://logo.clearbit.com/minimalist.com', 'Indian skincare brand known for science-backed, fragrance-free formulas with active ingredients at affordable prices.', 85, 70, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Dot & Key', 'India', 2018, NULL, 'Indian Brand', 1, 0, 0, 'https://www.dotandkey.com', 'https://logo.clearbit.com/dotandkey.com', 'Indian skincare brand offering gentle, skin-barrier-focused products with playful packaging and effective formulations.', 78, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('The Derma Co', 'India', 2021, Honasa Consumer, 'Indian Brand', 1, 0, 1, 'https://www.thedermaco.com', 'https://logo.clearbit.com/thedermaco.com', 'Indian derma-cosmetics brand offering clinically effective skincare products targeting acne, pigmentation, and aging.', 82, 65, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Plum', 'India', 2014, NULL, 'Indian Brand', 1, 1, 0, 'https://www.plumgoodness.com', 'https://logo.clearbit.com/plumgoodness.com', '100% vegan and cruelty-free Indian beauty brand offering skincare, haircare, and body care products.', 80, 80, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Deconstruct', 'India', 2021, NULL, 'Indian Brand', 1, 1, 1, 'https://www.deconstruct.com', 'https://logo.clearbit.com/deconstruct.com', 'Indian skincare brand focusing on transparent formulations with proven actives at concentration levels backed by research.', 72, 65, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Foxtale', 'India', 2021, NULL, 'Indian Brand', 1, 0, 0, 'https://www.foxtale.in', 'https://logo.clearbit.com/foxtale.in', 'Modern Indian skincare brand creating effective, aesthetic products targeting young consumers with skin concerns.', 75, 55, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Dr. Sheths', 'India', 2016, NULL, 'Indian Brand', 1, 0, 1, 'https://www.drsheths.com', 'https://logo.clearbit.com/drsheths.com', 'Indian skincare brand founded by a dermatologist, blending Ayurveda with modern science for effective formulations.', 70, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Pilgrim', 'India', 2019, NULL, 'Indian Brand', 1, 1, 0, 'https://www.pilgrim.com', 'https://logo.clearbit.com/pilgrim.com', 'Indian beauty brand offering international ingredient-based skincare, haircare, and body care at affordable prices.', 74, 60, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Aqualogica', 'India', 2021, Honasa Consumer, 'Indian Brand', 1, 0, 0, 'https://www.aqualogica.com', 'https://logo.clearbit.com/aqualogica.com', 'Hydration-focused Indian skincare brand offering water-based, lightweight formulas for all skin types.', 76, 60, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Mamaearth', 'India', 2016, Honasa Consumer, 'Indian Brand', 1, 1, 0, 'https://www.mamaearth.in', 'https://logo.clearbit.com/mamaearth.in', 'Indian toxin-free personal care brand offering natural skincare, haircare, and baby care products.', 88, 70, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('WOW Skin Science', 'India', 2016, WOW Science Labs, 'Indian Brand', 1, 0, 0, 'https://www.wowskin.com', 'https://logo.clearbit.com/wowskin.com', 'Indian personal care brand offering paraben-free, sulfate-free skincare and haircare products with natural actives.', 83, 60, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Biotique', 'India', 1992, Biotique, 'Indian Brand', 0, 0, 0, 'https://www.biotique.com', 'https://logo.clearbit.com/biotique.com', 'Ayurvedic beauty brand combining ancient Indian botanical recipes with modern biotechnology for effective skincare.', 75, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Lotus Herbals', 'India', 1993, Lotus Herbals, 'Indian Brand', 0, 0, 0, 'https://www.lotusbotanicals.com', 'https://logo.clearbit.com/lotusbotanicals.com', 'Indian herbal beauty brand offering skincare, sun care, and makeup products based on natural ingredients.', 78, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Himalaya', 'India', 1930, Himalaya Wellness, 'Indian Brand', 0, 0, 0, 'https://www.himalayawellness.in', 'https://logo.clearbit.com/himalayawellness.in', 'Pioneer in herbal healthcare and personal care, offering wellness products rooted in Ayurveda and modern science.', 82, 55, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Lakme', 'India', 1952, Hindustan Unilever, 'Indian Brand', 0, 0, 0, 'https://www.lakmeindia.com', 'https://logo.clearbit.com/lakmeindia.com', 'India''s leading cosmetics brand offering makeup, skincare, and beauty accessories for the Indian consumer.', 90, 50, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Forest Essentials', 'India', 2001, Forest Essentials, 'Indian Brand', 0, 0, 0, 'https://www.forestessentialsindia.com', 'https://logo.clearbit.com/forestessentialsindia.com', 'Luxury Ayurvedic skincare brand offering handcrafted products using traditional Indian beauty rituals and pure ingredients.', 76, 65, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Khadi Natural', 'India', 2001, Khadi Natural, 'Indian Brand', 1, 1, 0, 'https://www.khadinatural.com', 'https://logo.clearbit.com/khadinatural.com', 'Indian brand offering herbal and Ayurvedic skincare, haircare, and body care products under the Khadi umbrella.', 68, 60, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('mCaffeine', 'India', 2016, Raw Beauty Ventures, 'Indian Brand', 1, 1, 0, 'https://www.mcaffeine.com', 'https://logo.clearbit.com/mcaffeine.com', 'India''s first caffeinated personal care brand offering skincare and haircare products powered by coffee and other actives.', 80, 65, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Re equil', 'India', 2015, Re equil, 'Indian Brand', 1, 0, 1, 'https://www.reequil.com', 'https://logo.clearbit.com/reequil.com', 'Dermatologist-recommended Indian skincare brand offering clinically tested products for acne, pigmentation, and sensitive skin.', 77, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Earth Rhythm', 'India', 2019, Earth Rhythm, 'Indian Brand', 1, 1, 0, 'https://www.earthrhythm.com', 'https://logo.clearbit.com/earthrhythm.com', 'Indian clean beauty brand offering skincare, haircare, and body care with safe, transparent, and effective formulations.', 73, 75, 'Mid-range');

-- ============================================================
-- INTERNATIONAL BRANDS - DRUGSTORE (15)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('CeraVe', 'USA', 2005, L'Oreal, 'Drugstore', 0, 0, 1, 'https://www.cerave.com', 'https://logo.clearbit.com/cerave.com', 'Dermatologist-developed skincare brand known for ceramide-based formulas that restore and maintain the skin barrier.', 92, 55, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Cetaphil', 'USA', 1947, Galderma, 'Drugstore', 0, 0, 1, 'https://www.cetaphil.com', 'https://logo.clearbit.com/cetaphil.com', 'Gentle skincare brand recommended by dermatologists for sensitive skin, offering cleansers, moisturizers, and treatments.', 88, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Neutrogena', 'USA', 1930, Kenvue, 'Drugstore', 0, 0, 1, 'https://www.neutrogena.com', 'https://logo.clearbit.com/neutrogena.com', 'Dermatologist-recommended skincare brand offering cleansers, moisturizers, sunscreens, and acne treatments.', 90, 45, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Aveeno', 'USA', 1945, Kenvue, 'Drugstore', 0, 0, 1, 'https://www.aveeno.com', 'https://logo.clearbit.com/aveeno.com', 'Skincare brand harnessing the power of oat-based ingredients for gentle, effective solutions for sensitive skin.', 85, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Vanicream', 'USA', 1975, Vanicream, 'Drugstore', 0, 0, 1, 'https://www.vanicream.com', 'https://logo.clearbit.com/vanicream.com', 'Free-of skincare brand specifically formulated for sensitive skin, avoiding common chemical irritants.', 72, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Nivea', 'Germany', 1911, Beiersdorf, 'Drugstore', 0, 0, 0, 'https://www.nivea.com', 'https://logo.clearbit.com/nivea.com', 'German skincare brand offering moisturizers, sunscreens, and body care products for the entire family.', 90, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Olay', 'USA', 1952, Procter & Gamble, 'Drugstore', 0, 0, 0, 'https://www.olay.com', 'https://logo.clearbit.com/olay.com', 'Anti-aging skincare brand offering moisturizers, serums, and cleansers with science-backed ingredients.', 87, 45, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Dove', 'UK', 1957, Unilever, 'Drugstore', 0, 0, 0, 'https://www.dove.com', 'https://logo.clearbit.com/dove.com', 'Personal care brand known for gentle cleansing products and moisturizing body wash with real beauty messaging.', 88, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Garnier', 'France', 1904, L'Oreal, 'Drugstore', 0, 0, 0, 'https://www.garnier.com', 'https://logo.clearbit.com/garnier.com', 'French skincare and haircare brand offering affordable products infused with natural ingredients like green tea and Vitamin C.', 82, 55, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Maybelline', 'USA', 1915, L'Oreal, 'Drugstore', 0, 0, 0, 'https://www.maybelline.com', 'https://logo.clearbit.com/maybelline.com', 'World''s largest cosmetics brand offering affordable, trend-forward makeup products from mascara to foundation.', 90, 45, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('NYX', 'USA', 1999, L'Oreal, 'Drugstore', 1, 0, 0, 'https://www.nyxcosmetics.com', 'https://logo.clearbit.com/nyxcosmetics.com', 'Professional-quality, affordable makeup brand known for extensive shade ranges and trend-driven collections.', 85, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('e.l.f.', 'USA', 2004, e.l.f. Beauty, 'Drugstore', 1, 1, 0, 'https://www.elfcosmetics.com', 'https://logo.clearbit.com/elfcosmetics.com', 'Affordable, 100% vegan and cruelty-free makeup brand offering high-quality products at drugstore prices.', 84, 75, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Catrice', 'Germany', 2004, Cosnova Beauty, 'Drugstore', 0, 0, 0, 'https://www.catrice.com', 'https://logo.clearbit.com/catrice.com', 'German cosmetics brand offering trendy, affordable makeup products with European quality standards.', 68, 45, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Milani', 'USA', 2002, Milani Cosmetics, 'Drugstore', 0, 0, 0, 'https://www.milanicosmetics.com', 'https://logo.clearbit.com/milanicosmetics.com', 'Inclusive makeup brand offering high-quality, affordable products with extensive shade ranges for all skin tones.', 75, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('L.A. Girl', 'USA', 1985, L.A. Girl, 'Drugstore', 1, 0, 0, 'https://www.lagirl.com', 'https://logo.clearbit.com/lagirl.com', 'Affordable professional-quality makeup brand offering extensive color cosmetics, foundations, and concealers.', 65, 40, 'Budget');

-- ============================================================
-- INTERNATIONAL BRANDS - PREMIUM (15)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('La Roche-Posay', 'France', 1975, L'Oreal, 'Premium', 0, 0, 1, 'https://www.laroche-posay.com', 'https://logo.clearbit.com/laroche-posay.com', 'Dermatologist-recommended French skincare brand using thermal spring water for sensitive and problem skin.', 90, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Bioderma', 'France', 1977, NAOS, 'Premium', 0, 0, 1, 'https://www.bioderma.com', 'https://logo.clearbit.com/bioderma.com', 'French dermatological skincare brand using biology-inspired formulas to respect skin ecology and strengthen natural processes.', 85, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Eucerin', 'Germany', 1900, Beiersdorf, 'Premium', 0, 0, 1, 'https://www.eucerin.com', 'https://logo.clearbit.com/eucerin.com', 'German dermatological skincare brand offering science-based solutions for sensitive, dry, and aging skin.', 84, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Vichy', 'France', 1931, L'Oreal, 'Premium', 0, 0, 1, 'https://www.vichy.com', 'https://logo.clearbit.com/vichy.com', 'French pharmacy brand harnessing volcanic mineralizing water for anti-aging and sensitive skin solutions.', 78, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('SVR', 'France', 1962, SVR Laboratoire, 'Premium', 1, 0, 1, 'https://www.svr.com', 'https://logo.clearbit.com/svr.com', 'French dermo-cosmetic brand offering dermatologist-tested skincare for sensitive and reactive skin types.', 68, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Avene', 'France', 1990, Pierre Fabre, 'Premium', 0, 0, 1, 'https://www.avene.com', 'https://logo.clearbit.com/avene.com', 'French thermal water-based skincare brand specializing in products for sensitive, intolerant, and allergic skin.', 82, 60, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Paula''s Choice', 'USA', 1995, Paula''s Choice, 'Premium', 1, 1, 0, 'https://www.paulaschoice.com', 'https://logo.clearbit.com/paulaschoice.com', 'Research-driven skincare brand offering effective, fragrance-free formulas with proven ingredients like BHA and retinol.', 88, 70, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('The Ordinary', 'Canada', 2016, DECIEM, 'Premium', 1, 1, 0, 'https://www.theordinary.com', 'https://logo.clearbit.com/theordinary.com', 'Clinical skincare brand offering single-ingredient formulations at transparent, affordable prices with no frills.', 92, 70, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Simple', 'UK', 1960, Unilever, 'Premium', 0, 0, 0, 'https://www.simple.co.uk', 'https://logo.clearbit.com/simple.co.uk', 'Gentle skincare brand formulated for sensitive skin with no artificial perfumes, dyes, or harsh chemicals.', 75, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('ROC', 'USA', 1959, Revlon, 'Premium', 0, 0, 0, 'https://www.rocskincare.com', 'https://logo.clearbit.com/rocskincare.com', 'Dermatologist-recommended anti-aging skincare brand offering retinol-based products for visible results.', 72, 45, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('La Mer', 'USA', 1965, Estee Lauder Companies, 'Premium', 0, 0, 0, 'https://www.lamer.com', 'https://logo.clearbit.com/lamer.com', 'Ultra-luxury skincare brand known for its legendary Miracle Broth andCell Renewal Serum.', 85, 40, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Estee Lauder', 'USA', 1946, Estee Lauder Companies, 'Premium', 0, 0, 0, 'https://www.esteelauder.com', 'https://logo.clearbit.com/esteelauder.com', 'Iconic American luxury beauty brand offering skincare, makeup, and fragrance products for sophisticated consumers.', 88, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Clinique', 'USA', 1968, Estee Lauder Companies, 'Premium', 0, 0, 1, 'https://www.clinique.com', 'https://logo.clearbit.com/clinique.com', 'Allergy-tested, 100% fragrance-free skincare brand offering dermatologist-developed products for every skin type.', 86, 50, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Shiseido', 'Japan', 1872, Shiseido Company, 'Premium', 0, 0, 0, 'https://www.shiseido.com', 'https://logo.clearbit.com/shiseido.com', 'Japanese luxury cosmetics brand combining Eastern wisdom with Western science for innovative skincare and makeup.', 87, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('MAC Cosmetics', 'Canada', 1984, Estee Lauder Companies, 'Premium', 0, 0, 0, 'https://www.maccosmetics.com', 'https://logo.clearbit.com/maccosmetics.com', 'Professional artistry makeup brand known for extensive color ranges, high-performance formulas, and runway-inspired collections.', 88, 45, 'Premium');

-- ============================================================
-- INTERNATIONAL BRANDS - LUXURY (10)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('SK-II', 'Japan', 1980, Procter & Gamble, 'Luxury', 0, 0, 0, 'https://www.sk-ii.com', 'https://logo.clearbit.com/sk-ii.com', 'Japanese luxury skincare brand centered around Pitera, a natural bio-ingredient derived from yeast fermentation.', 82, 45, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Sulwhasoo', 'South Korea', 1966, Amorepacific, 'Luxury', 0, 0, 0, 'https://www.sulwhasoo.com', 'https://logo.clearbit.com/sulwhasoo.com', 'Korean luxury skincare brand blending Korean herbal medicine (Jaumdan) with modern anti-aging science.', 78, 50, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('La Prairie', 'Switzerland', 1931, Beiersdorf, 'Luxury', 0, 0, 0, 'https://www.laprairie.com', 'https://logo.clearbit.com/laprairie.com', 'Ultra-luxury Swiss skincare brand known for rare ingredients like caviar, gold, and platinum in opulent formulations.', 75, 40, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Tom Ford Beauty', 'USA', 2006, Estee Lauder Companies, 'Luxury', 0, 0, 0, 'https://www.tomford.com', 'https://logo.clearbit.com/tomford.com', 'Luxury beauty brand offering opulent skincare, makeup, and fragrances with Tom Ford''s signature bold aesthetic.', 80, 35, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Charlotte Tilbury', 'UK', 2013, Puig, 'Luxury', 0, 0, 0, 'https://www.charlottetilbury.com', 'https://logo.clearbit.com/charlottetilbury.com', 'British luxury makeup brand offering red-carpet-inspired products with Hollywood glamour and innovative formulas.', 88, 45, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('YSL Beauty', 'France', 1978, L''Oreal, 'Luxury', 0, 0, 0, 'https://www.yslbeauty.com', 'https://logo.clearbit.com/yslbeauty.com', 'French luxury beauty brand offering haute couture makeup, skincare, and fragrances with Yves Saint Laurent''s iconic style.', 85, 45, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Chanel Beauty', 'France', 1924, Chanel, 'Luxury', 0, 0, 0, 'https://www.chanel.com', 'https://logo.clearbit.com/chanel.com', 'Iconic French luxury house offering timeless beauty products with elegant formulations and sophisticated packaging.', 87, 45, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Dior Beauty', 'France', 1947, LVMH, 'Luxury', 0, 0, 0, 'https://www.dior.com', 'https://logo.clearbit.com/dior.com', 'French luxury beauty brand offering couture makeup, skincare, and fragrances with Christian Dior''s legendary elegance.', 88, 45, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Guerlain', 'France', 1828, LVMH, 'Luxury', 0, 0, 0, 'https://www.guerlain.com', 'https://logo.clearbit.com/guerlain.com', 'Historic French luxury beauty house offering premium skincare, makeup, and fragrances with exceptional craftsmanship.', 78, 50, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Hermes Beauty', 'France', 1999, Hermes International, 'Luxury', 0, 0, 0, 'https://www.hermes.com', 'https://logo.clearbit.com/hermes.com', 'French luxury maison offering refined beauty products with understated elegance and exceptional quality.', 72, 50, 'Luxury');

-- ============================================================
-- INTERNATIONAL BRANDS - K-BEAUTY (15)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('COSRX', 'South Korea', 2013, COSRX, 'Korean Beauty', 1, 0, 0, 'https://www.cosrx.com', 'https://logo.clearbit.com/cosrx.com', 'Korean skincare brand offering simple, effective products with high concentrations of active ingredients like snail mucin and BHA.', 90, 65, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Beauty of Joseon', 'South Korea', 2018, Beauty of Joseon, 'Korean Beauty', 1, 1, 0, 'https://www.beautyofjoseon.com', 'https://logo.clearbit.com/beautyofjoseon.com', 'Korean skincare brand inspired by Korean herbal medicine (Hanbang), offering gentle formulas with traditional ingredients.', 85, 70, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Isntree', 'South Korea', 2017, Isntree, 'Korean Beauty', 1, 1, 0, 'https://www.isntree.com', 'https://logo.clearbit.com/isntree.com', 'Korean skincare brand using plant-derived ingredients to create gentle, effective products for sensitive skin.', 76, 70, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Innisfree', 'South Korea', 2000, Amorepacific, 'Korean Beauty', 0, 0, 0, 'https://www.innisfree.com', 'https://logo.clearbit.com/innisfree.com', 'Korean natural skincare brand using ingredients from Jeju Island, offering eco-friendly products with volcanic clay and green tea.', 82, 70, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Laneige', 'South Korea', 1994, Amorepacific, 'Korean Beauty', 0, 0, 0, 'https://www.laneige.com', 'https://logo.clearbit.com/laneige.com', 'Korean water science skincare brand known for its Water Sleeping Mask and lip sleeping masks for deep hydration.', 86, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Etude', 'South Korea', 1969, Amorepacific, 'Korean Beauty', 0, 0, 0, 'https://www.etudehouse.com', 'https://logo.clearbit.com/etudehouse.com', 'Playful Korean beauty brand offering affordable, fun makeup and skincare products with a girly aesthetic.', 74, 55, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Banila Co', 'South Korea', 2005, Able C&C, 'Korean Beauty', 0, 0, 0, 'https://www.banilaco.com', 'https://logo.clearbit.com/banilaco.com', 'Korean makeup and skincare brand famous for its Clean It Zero cleansing balm and base makeup products.', 75, 50, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Missha', 'South Korea', 2000, Able C&C, 'Korean Beauty', 0, 0, 0, 'https://www.missha.com', 'https://logo.clearbit.com/missha.com', 'Korean skincare brand offering affordable, effective products with fermented ingredients and advanced Korean formulations.', 78, 55, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Nature Republic', 'South Korea', 2009, Nature Republic, 'Korean Beauty', 0, 0, 0, 'https://www.naturerepublic.com', 'https://logo.clearbit.com/naturerepublic.com', 'Korean skincare brand using natural plant-based ingredients, known for its soothing aloe vera gel and skincare products.', 73, 55, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Tony Moly', 'South Korea', 2006, Tony Moly, 'Korean Beauty', 0, 0, 0, 'https://www.tonymoly.com', 'https://logo.clearbit.com/tonymoly.com', 'Fun Korean beauty brand known for its playful, cute packaging and innovative skincare products like sheet masks.', 74, 50, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Holika Holika', 'South Korea', 2010, Enprani, 'Korean Beauty', 0, 0, 0, 'https://www.holikaholika.com', 'https://logo.clearbit.com/holikaholika.com', 'Korean beauty brand offering whimsical, affordableskincare and makeup products with unique formulations.', 65, 45, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Some By Mi', 'South Korea', 2015, Some By Mi, 'Korean Beauty', 1, 0, 0, 'https://www.somebymi.com', 'https://logo.clearbit.com/somebymi.com', 'Korean skincare brand specializing in acne-fighting products with AHA, BHA, PHA and tea tree oil.', 80, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Dear Klairs', 'South Korea', 2010, Wish Company, 'Korean Beauty', 1, 1, 0, 'https://www.klairs.com', 'https://logo.clearbit.com/klairs.com', 'Korean skincare brand for sensitive skin offering gentle, vegan products with minimal, effective ingredients.', 82, 75, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Neogen', 'South Korea', 2009, Neogen Lab, 'Korean Beauty', 1, 0, 0, 'https://www.neogenlab.com', 'https://logo.clearbit.com/neogenlab.com', 'Innovative Korean skincare brand known for its bio-technical formulations and unique delivery systems.', 74, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Pyunkang Yul', 'South Korea', 2015, Pyunkang Korean Medicine Clinic, 'Korean Beauty', 1, 1, 0, 'https://www.pyunkangyul.com', 'https://logo.clearbit.com/pyunkangyul.com', 'Korean skincare brand from a traditional medicine clinic, offering minimalist formulas focusing on skin barrier health.', 76, 70, 'Mid-range');

-- ============================================================
-- INTERNATIONAL BRANDS - CLINICAL / DERMATOLOGIST (15)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('SkinCeuticals', 'USA', 1997, L'Oreal, 'Clinical', 0, 0, 1, 'https://www.skinceuticals.com', 'https://logo.clearbit.com/skinceuticals.com', 'Advanced skincare brand backed by science, offering antioxidants, retinols, and clinical treatments for optimal skin health.', 88, 50, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('iS Clinical', 'USA', 2002, Innovative Skincare, 'Clinical', 1, 0, 1, 'https://www.isclinical.com', 'https://logo.clearbit.com/isclinical.com', 'Clinical skincare brand combining botanical ingredients with pharmaceutical-grade science for transformative results.', 72, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Drunk Elephant', 'USA', 2012, Shiseido, 'Clinical', 1, 1, 0, 'https://www.drunkelephant.com', 'https://logo.clearbit.com/drunkelephant.com', 'Clean-compatible skincare brand avoiding the Suspicious 6, offering effective formulas with biocompatible ingredients.', 88, 60, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Tatcha', 'USA', 2009, Unilever, 'Clinical', 1, 0, 0, 'https://www.tatcha.com', 'https://logo.clearbit.com/tatcha.com', 'Japanese-inspired luxury skincare brand using ancient geisha beauty rituals and superfoods like green tea, rice, and algae.', 82, 60, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Sunday Riley', 'USA', 2009, Sunday Riley, 'Clinical', 1, 0, 0, 'https://www.sundayriley.com', 'https://logo.clearbit.com/sundayriley.com', 'Botanically-based skincare brand offering potent, fast-acting formulas with natural plant extracts and cutting-edge science.', 82, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Ole Henriksen', 'USA', 1975, Kendo Holdings, 'Clinical', 1, 0, 0, 'https://www.olehenriksen.com', 'https://logo.clearbit.com/olehenriksen.com', 'Danish-American skincare brand offering vitamin C-powered products with a spa-inspired, results-driven approach.', 76, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Philosophy', 'USA', 1996, Coty, 'Clinical', 0, 0, 0, 'https://www.philosophy.com', 'https://logo.clearbit.com/philosophy.com', 'Skincare brand combining science and philosophy, offering gentle cleansers, moisturizers, and targeted treatments.', 72, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Dermalogica', 'USA', 1986, Unilever, 'Clinical', 1, 0, 1, 'https://www.dermalogica.com', 'https://logo.clearbit.com/dermalogica.com', 'Professional-grade skincare brand used by estheticians worldwide, offering science-backed formulas for skin health.', 80, 60, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('bareMinerals', 'USA', 1995, Shiseido, 'Clinical', 1, 0, 0, 'https://www.bareminerals.com', 'https://logo.clearbit.com/bareminerals.com', 'Clean mineral makeup brand offering clean beauty products with mineral-based formulas for natural-looking coverage.', 75, 65, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('IT Cosmetics', 'USA', 2008, L''Oreal, 'Clinical', 0, 0, 1, 'https://www.itcosmetics.com', 'https://logo.clearbit.com/itcosmetics.com', 'Clinical skincare and makeup brand developed with plastic surgeons, offering problem-solving products with anti-aging ingredients.', 82, 50, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Peter Thomas Roth', 'USA', 1993, Peter Thomas Roth, 'Clinical', 0, 0, 0, 'https://www.peterthomasroth.com', 'https://logo.clearbit.com/peterthomasroth.com', 'Clinical skincare brand offering potent, results-driven treatments with ingredients like retinol, hyaluronic acid, and Vitamin C.', 78, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('First Aid Beauty', 'USA', 2009, Procter & Gamble, 'Clinical', 1, 0, 0, 'https://www.firstaidbeauty.com', 'https://logo.clearbit.com/firstaidbeauty.com', 'Sensitive skin skincare brand offering clean, safe formulas free from harsh chemicals and common irritants.', 80, 60, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Murad', 'USA', 1989, Unilever, 'Clinical', 0, 0, 1, 'https://www.murad.com', 'https://logo.clearbit.com/murad.com', 'Clinical skincare brand founded by a dermatologist, offering science-based solutions for acne, aging, and environmental damage.', 78, 50, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Origins', 'USA', 1990, Estee Lauder Companies, 'Clinical', 1, 0, 0, 'https://www.origins.com', 'https://logo.clearbit.com/origins.com', 'Nature-inspired skincare brand combining plant science and powerful formulas with eco-friendly packaging and practices.', 76, 65, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Kiehls', 'USA', 1851, L''Oreal, 'Clinical', 0, 0, 0, 'https://www.kiehls.com', 'https://logo.clearbit.com/kiehls.com', 'New York apothecary-inspired skincare brand offering natural formulas with ingredients like calendula, squalane, and Vitamin C.', 80, 55, 'Premium');

-- ============================================================
-- INTERNATIONAL BRANDS - ORGANIC / INDIAN (9 new)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Kama Ayurveda', 'India', 2002, Kama Ayurveda, 'Organic', 0, 0, 0, 'https://www.kamaayurveda.com', 'https://logo.clearbit.com/kamaayurveda.com', 'Premium Ayurvedic brand offering authentic, traditional Indian beauty and wellness products with pure natural ingredients.', 75, 70, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Organic Harvest', 'India', 2013, Organic Harvest, 'Organic', 1, 1, 0, 'https://www.organicharvest.in', 'https://logo.clearbit.com/organicharvest.in', 'Indian organic skincare brand offering certified organic products for skin, hair, and body care.', 65, 80, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Just Herbs', 'India', 2010, Just Herbs, 'Organic', 1, 1, 0, 'https://www.justherbs.in', 'https://logo.clearbit.com/justherbs.in', 'Indian ayurvedic beauty brand offering handcrafted, preservative-free skincare and haircare with traditional herbs.', 70, 75, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Soultree', 'India', 2012, Soultree, 'Organic', 1, 1, 0, 'https://www.soultree.in', 'https://logo.clearbit.com/soultree.in', 'Indian organic brand offering BIS-certified organic personal care products inspired by Ayurvedic traditions.', 58, 80, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Bio Basics', 'India', 2015, Bio Basics, 'Organic', 1, 1, 0, 'https://www.biobasics.in', 'https://logo.clearbit.com/biobasics.in', 'Indian organic lifestyle brand offering organic skincare, haircare, and wellness products with clean ingredients.', 50, 85, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Neemli Naturals', 'India', 2016, Neemli Naturals, 'Organic', 1, 1, 0, 'https://www.neemli.com', 'https://logo.clearbit.com/neemli.com', 'Indian artisanal skincare brand offering small-batch, handcrafted products with organic and natural ingredients.', 55, 80, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Juicy Chemistry', 'India', 2014, Juicy Chemistry, 'Organic', 1, 1, 0, 'https://www.juicychemistry.com', 'https://logo.clearbit.com/juicychemistry.com', 'Indian organic beauty brand offering USDA-certified organic, cold-pressed skincare and haircare products.', 62, 85, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Rubara', 'India', 2018, Rubara, 'Organic', 1, 1, 0, 'https://www.rubara.com', 'https://logo.clearbit.com/rubara.com', 'Indian clean beauty brand offering plant-based, organic skincare products with a focus on sustainability.', 48, 80, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Old Tree', 'India', 2017, Old Tree, 'Organic', 1, 1, 0, 'https://www.oldtree.in', 'https://logo.clearbit.com/oldtree.in', 'Indian organic wellness brand offering herbal and natural personal care products inspired by traditional Indian remedies.', 42, 75, 'Budget');

-- ============================================================
-- INTERNATIONAL BRANDS - ADDITIONAL (20)
-- ============================================================

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Fenty Beauty', 'USA', 2017, Kendo Holdings, 'Premium', 1, 0, 0, 'https://www.fentybeauty.com', 'https://logo.clearbit.com/fentybeauty.com', 'Rihanna''s beauty brand offering inclusive shade ranges and innovative formulas for all skin tones and types.', 90, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Rare Beauty', 'USA', 2020, Kendo Holdings, 'Premium', 1, 0, 0, 'https://www.rarebeauty.com', 'https://logo.clearbit.com/rarebeauty.com', 'Selena Gomez''s beauty brand focusing on mental health awareness with easy-to-use, feel-good makeup products.', 86, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Tarte', 'USA', 1999, Kosé Corporation, 'Premium', 1, 0, 0, 'https://www.tartecosmetics.com', 'https://logo.clearbit.com/tartecosmetics.com', 'Eco-chic beauty brand offering high-performance makeup and skincare with natural ingredients like Amazonian clay.', 80, 60, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Too Faced', 'USA', 1998, Estee Lauder Companies, 'Premium', 0, 0, 0, 'https://www.toofaced.com', 'https://logo.clearbit.com/toofaced.com', 'Fun, playful makeup brand offering feminine products with innovative formulas and whimsical packaging.', 82, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Benefit Cosmetics', 'USA', 1976, LVMH, 'Premium', 0, 0, 0, 'https://www.benefitcosmetics.com', 'https://logo.clearbit.com/benefitcosmetics.com', 'San Francisco-based beauty brand famous for brow products, mascaras, and cheek products with retro-glam packaging.', 85, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Urban Decay', 'USA', 1996, L''Oreal, 'Premium', 0, 0, 0, 'https://www.urbandecay.com', 'https://logo.clearbit.com/urbandecay.com', 'Edgy beauty brand known for its Naked palettes, long-lasting formulas, and bold, rule-breaking color cosmetics.', 84, 50, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('NARS', 'France', 1994, Shiseido, 'Premium', 0, 0, 0, 'https://www.narscosmetics.com', 'https://logo.clearbit.com/narscosmetics.com', 'French-American luxury makeup brand known for bold, sophisticated color cosmetics and iconicOrgasm blush.', 84, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Huda Beauty', 'USA', 2013, Huda Beauty, 'Premium', 0, 0, 0, 'https://www.hudabeauty.com', 'https://logo.clearbit.com/hudabeauty.com', 'Huda Kattan''s beauty empire offering inclusive makeup, skincare, and fragrance products with Middle Eastern glamour.', 86, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Pat McGrath Labs', 'USA', 2015, Pat McGrath Labs, 'Luxury', 0, 0, 0, 'https://www.patmcgrath.com', 'https://logo.clearbit.com/patmcgrath.com', 'Visionary makeup artist brand offering avant-garde, high-pigment products with editorial-worthy formulas.', 78, 40, 'Luxury');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Morphe', 'USA', 2008, Forma Brands, 'Drugstore', 0, 0, 0, 'https://www.morphe.com', 'https://logo.clearbit.com/morphe.com', 'Affordable makeup brand known for professional-quality brush sets and trend-driven palettes favored by beauty influencers.', 80, 40, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('ColourPop', 'USA', 2014, Seed Beauty, 'Drugstore', 1, 1, 0, 'https://www.colourpop.com', 'https://logo.clearbit.com/colourpop.com', 'Ultra-affordable makeup brand offering trendy, high-quality products with frequent launches and collaborations.', 84, 60, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Anastasia Beverly Hills', 'USA', 1997, Anastasia Beverly Hills, 'Premium', 0, 0, 0, 'https://www.anastasiabeverlyhills.com', 'https://logo.clearbit.com/anastasiabeverlyhills.com', 'Brow-centric beauty brand known for perfecting the art of eyebrow shaping and offering luxurious makeup products.', 82, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Wet n Wild', 'USA', 1979, Markwins Beauty, 'Drugstore', 0, 0, 0, 'https://www.wetnwildbeauty.com', 'https://logo.clearbit.com/wetnwildbeauty.com', 'Budget-friendly cosmetics brand offering quality makeup at ultra-low prices with a wide product range.', 72, 35, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Revlon', 'USA', 1932, Revlon, 'Drugstore', 0, 0, 0, 'https://www.revlon.com', 'https://logo.clearbit.com/revlon.com', 'Iconic American beauty brand offering color cosmetics, skincare, and fragrances with a heritage of innovation.', 80, 40, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Almay', 'USA', 1931, Revlon, 'Drugstore', 0, 0, 0, 'https://www.almay.com', 'https://logo.clearbit.com/almay.com', 'Hypoallergenic beauty brand offering gentle, allergy-tested makeup suitable for sensitive skin and contact lens wearers.', 60, 45, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Bobbi Brown', 'USA', 1991, Estee Lauder Companies, 'Premium', 0, 0, 0, 'https://www.bobbibrown.com', 'https://logo.clearbit.com/bobbibrown.com', 'Effortless beauty brand celebrating natural beauty with skin-first makeup and inclusive shade ranges.', 80, 50, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Laura Mercier', 'Canada', 1996, Shiseido, 'Premium', 0, 0, 0, 'https://www.lauramercier.com', 'https://logo.clearbit.com/lauramercier.com', 'French-inspired beauty brand known for the iconic Translucent Loose Setting Powder and flawless face makeup.', 78, 45, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Dr. Jart', 'South Korea', 2004, Estee Lauder Companies, 'Clinical', 0, 0, 1, 'https://www.drjart.com', 'https://logo.clearbit.com/drjart.com', 'Korean derma-cosmetic brand combining dermatological science with art, offering innovative skincare like Cicapair and Ceramidin.', 82, 55, 'Premium');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Glossier', 'USA', 2014, Glossier, 'Premium', 1, 0, 0, 'https://www.glossier.com', 'https://logo.clearbit.com/glossier.com', 'Minimalist beauty brand creating effortless, skin-first products inspired by real people and real beauty routines.', 85, 60, 'Mid-range');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Juno & Co', 'USA', 2018, Juno & Co, 'Drugstore', 1, 1, 0, 'https://www.junoandco.com', 'https://logo.clearbit.com/junoandco.com', 'Affordable clean beauty brand offering vegan makeup and skincare with a focus on sustainable, reef-safe formulas.', 55, 80, 'Budget');

INSERT INTO brands (company_name, country, founded_year, parent_company, brand_type, cruelty_free, vegan_products, dermatologist_recommended, official_website, logo_url, description, popularity_score, sustainability_score, average_price_range)
VALUES ('Pai Skincare', 'UK', 2007, Pai Skincare, 'Organic', 1, 1, 0, 'https://www.paiskincare.com', 'https://logo.clearbit.com/paiskincare.com', 'British organic skincare brand offering certified organic products specifically formulated for sensitive and reactive skin.', 60, 85, 'Premium');
