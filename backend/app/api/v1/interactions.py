from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import random
import hashlib

router = APIRouter(prefix="/interactions", tags=["Ingredient Interaction Checker"])


# ── Interaction Database ─────────────────────────────────────────────

INTERACTIONS_DB: List[Dict[str, Any]] = [
    {"a": "retinol", "b": "glycolic acid", "severity": "avoid", "description": "Retinol and glycolic acid both increase skin cell turnover. Combined, they cause severe irritation, peeling, and compromised skin barrier.", "recommendation": "Use glycolic acid in the morning and retinol at night, or alternate nights.", "scientific_basis": "Both act on keratinocyte differentiation pathways. Over-exfoliation leads to transepidermal water loss (TEWL) and inflammation."},
    {"a": "retinol", "b": "lactic acid", "severity": "avoid", "description": "Lactic acid is an AHA that, combined with retinol, can cause excessive irritation and barrier damage.", "recommendation": "Alternate nights or use on different days.", "scientific_basis": "AHAs thin the stratum corneum while retinol accelerates cell turnover, compounding irritation."},
    {"a": "retinol", "b": "salicylic acid", "severity": "avoid", "description": "BHA (salicylic acid) and retinol together cause extreme dryness, redness, and peeling.", "recommendation": "Use salicylic acid cleanser in the morning, retinol at night.", "scientific_basis": "Salicylic acid penetrates pores and dissolves sebum while retinol thins the outer skin layer, leading to excessive penetration and irritation."},
    {"a": "retinol", "b": "benzoyl peroxide", "severity": "avoid", "description": "Benzoyl peroxide oxidizes retinol, completely deactivating it. You get irritation without the benefit.", "recommendation": "Use benzoyl peroxide in the morning, retinol at night. Never mix in the same routine.", "scientific_basis": "BPO is a strong oxidizing agent that degrades retinol through oxidative decomposition."},
    {"a": "retinol", "b": "vitamin c", "severity": "caution", "description": "Both are potent actives that can irritate sensitive skin when used together. They also work at different optimal pH levels.", "recommendation": "Use vitamin C in the morning and retinol at night for best results.", "scientific_basis": "L-ascorbic acid works best at pH 2.5-3.5 while retinol is most effective at pH 5.5-6. Combining can destabilize both."},
    {"a": "retinol", "b": "aha", "severity": "avoid", "description": "AHAs like glycolic, lactic, and mandelic acid combined with retinol cause severe irritation and barrier disruption.", "recommendation": "Alternate days or use AHA in morning and retinol at night.", "scientific_basis": "Both exfoliate through different mechanisms, compounding the effect and increasing TEWL."},
    {"a": "retinol", "b": "bha", "severity": "avoid", "description": "BHA combined with retinol over-exfoliates and damages the skin barrier.", "recommendation": "Use on separate days or different times.", "scientific_basis": "BHA's oil-soluble exfoliation plus retinol's cellular turnover creates excessive exfoliation."},
    {"a": "vitamin c", "b": "niacinamide", "severity": "synergistic", "description": "Modern research shows these work excellently together. Vitamin C provides antioxidant protection while niacinamide strengthens the skin barrier.", "recommendation": "Great combination! Apply vitamin C first, then niacinamide.", "scientific_basis": "Vitamin C brightens through tyrosinase inhibition while niacinamide reduces melanin transfer. Together they provide comprehensive brightening. The old myth of flushing has been debunked at modern formulation pH levels."},
    {"a": "vitamin c", "b": "hyaluronic acid", "severity": "synergistic", "description": "Hyaluronic acid hydrates and plumps while vitamin C provides antioxidant protection. They work perfectly together.", "recommendation": "Apply hyaluronic acid on damp skin, then vitamin C serum on top.", "scientific_basis": "HA provides a hydrated base that helps vitamin C penetrate while the antioxidant protects HA from degradation."},
    {"a": "vitamin c", "b": "vitamin e", "severity": "synergistic", "description": "Vitamin C and E work synergistically to boost each other's antioxidant capacity by 4x.", "recommendation": "Use together for maximum antioxidant protection.", "scientific_basis": "Vitamin C regenerates oxidized vitamin E, while vitamin E stabilizes vitamin C. This redox cycling amplifies photoprotection."},
    {"a": "vitamin c", "b": "ferulic acid", "severity": "synergistic", "description": "Ferulic acid stabilizes vitamin C and E, doubling their photoprotection. The gold-standard antioxidant combination.", "recommendation": "Look for serums containing all three (C+E+Ferulic).", "scientific_basis": "Ferulic acid is a plant-based antioxidant that absorbs UV light and stabilizes the C+E complex, increasing efficacy by 8x."},
    {"a": "vitamin c", "b": "retinol", "severity": "caution", "description": "Both are powerful actives. Using together can overwhelm sensitive skin.", "recommendation": "Use vitamin C in the morning, retinol at night.", "scientific_basis": "Different optimal pH requirements and both can cause irritation independently."},
    {"a": "vitamin c", "b": "glycolic acid", "severity": "avoid", "description": "Low pH of vitamin C combined with glycolic acid causes significant irritation and stinging.", "recommendation": "Use glycolic acid at night, vitamin C in the morning.", "scientific_basis": "Both require acidic pH to function, and combining two acids can drop pH too low, causing chemical burns."},
    {"a": "vitamin c", "b": "aha", "severity": "avoid", "description": "Combining vitamin C with any AHA creates excessive acidity and irritation.", "recommendation": "Use at different times of day.", "scientific_basis": "AHAs at low pH + vitamin C at low pH = combined acid load that damages the skin barrier."},
    {"a": "niacinamide", "b": "aha", "severity": "caution", "description": "At very low pH (below 5), niacinamide can convert to niacin, causing flushing and irritation.", "recommendation": "Use niacinamide first, wait 10-15 minutes, then apply AHA. Or use at different times.", "scientific_basis": "Niacinamide hydrolyzes to nicotinic acid at pH < 5. Modern formulations buffer this, but layering can still cause issues."},
    {"a": "niacinamide", "b": "vitamin c", "severity": "synergistic", "description": "Excellent combination for brightening and reducing hyperpigmentation through complementary pathways.", "recommendation": "Great together! Apply vitamin C first, then niacinamide.", "scientific_basis": "Vitamin C inhibits tyrosinase while niacinamide blocks melanosome transfer to keratinocytes."},
    {"a": "niacinamide", "b": "retinol", "severity": "synergistic", "description": "Niacinamide soothes retinol irritation while providing additional anti-aging benefits.", "recommendation": "Perfect pairing! Apply niacinamide with or before retinol.", "scientific_basis": "Niacinamide strengthens ceramide production, offsetting retinol's barrier-weakening effects."},
    {"a": "niacinamide", "b": "hyaluronic acid", "severity": "synergistic", "description": "Niacinamide strengthens the skin barrier while hyaluronic acid provides deep hydration. Perfect together.", "recommendation": "Apply HA first for hydration, then niacinamide to lock it in.", "scientific_basis": "HA plumps with water while niacinamide increases ceramide and fatty acid production in the barrier."},
    {"a": "aha", "b": "bha", "severity": "caution", "description": "Using AHA and BHA together increases risk of over-exfoliation, redness, and irritation.", "recommendation": "If you must use both, start with low concentrations and use BHA first to clear pores, then AHA on top.", "scientific_basis": "AHAs work on the skin surface while BHAs penetrate into pores. Together they exfoliate both surface and within, potentially overwhelming the skin."},
    {"a": "aha", "b": "vitamin c", "severity": "avoid", "description": "Combining these low-pH ingredients creates excessive acidity and chemical irritation.", "recommendation": "Use vitamin C in the morning, AHA at night.", "scientific_basis": "Both require pH below 4 to be effective. Combined, the acid load is too much for most skin."},
    {"a": "aha", "b": "retinol", "severity": "avoid", "description": "AHA plus retinol leads to extreme irritation, peeling, and potential chemical burns.", "recommendation": "Alternate nights or use different days.", "scientific_basis": "Surface exfoliation from AHA combined with deep cellular turnover from retinol is too aggressive."},
    {"a": "bha", "b": "benzoyl peroxide", "severity": "caution", "description": "Both are anti-acne powerhouses but can cause severe dryness and irritation together.", "recommendation": "Start with one, add the other gradually. Never use at the same time initially.", "scientific_basis": "BHA clears pores while BPO kills bacteria. Both are drying, and combined use can compromise the barrier."},
    {"a": "bha", "b": "retinol", "severity": "avoid", "description": "Double exfoliation and irritation from BHA and retinol combined.", "recommendation": "Use BHA in the morning, retinol at night.", "scientific_basis": "BHA penetrates pores while retinol accelerates turnover, creating excessive exfoliation."},
    {"a": "hyaluronic acid", "b": "retinol", "severity": "synergistic", "description": "HA provides essential hydration that counteracts retinol's drying effects.", "recommendation": "Always pair retinol with HA for best tolerance.", "scientific_basis": "HA's humectant properties maintain hydration while retinol works on cellular turnover."},
    {"a": "hyaluronic acid", "b": "niacinamide", "severity": "synergistic", "description": "The ultimate hydration-barrier duo. HA draws moisture in, niacinamide seals it.", "recommendation": "Apply HA on damp skin, then niacinamide serum.", "scientific_basis": "HA binds 1000x its weight in water; niacinamide increases lipid barrier production."},
    {"a": "hyaluronic acid", "b": "glycolic acid", "severity": "synergistic", "description": "HA hydrates after AHA exfoliation, preventing the dryness that AHAs can cause.", "recommendation": "Apply AHA first, wait 15 minutes, then HA.", "scientific_basis": "AHAs remove dead cells and HA hydrates the fresh skin underneath."},
    {"a": "hyaluronic acid", "b": "peptides", "severity": "synergistic", "description": "HA provides the hydrated environment peptides need to function optimally.", "recommendation": "Great combination for anti-aging routines.", "scientific_basis": "Peptides signal collagen production best in hydrated environments."},
    {"a": "hyaluronic acid", "b": "vitamin c", "severity": "synergistic", "description": "HA hydrates while vitamin C protects and brightens. Perfect layering combo.", "recommendation": "Apply HA first on damp skin, then vitamin C.", "scientific_basis": "Hydrated skin absorbs vitamin C more effectively."},
    {"a": "peptides", "b": "aha", "severity": "caution", "description": "Low pH from AHAs can break down peptide bonds, reducing their efficacy.", "recommendation": "Use peptides in the morning, AHAs at night.", "scientific_basis": "Peptides are chains of amino acids that can be cleaved at low pH conditions."},
    {"a": "peptides", "b": "bha", "severity": "caution", "description": "BHAs can denature peptides at low pH, making them ineffective.", "recommendation": "Use at different times of day.", "scientific_basis": "Salicylic acid's acidic pH can hydrolyze peptide bonds."},
    {"a": "peptides", "b": "retinol", "severity": "synergistic", "description": "Peptides and retinol both boost collagen through different pathways. Excellent anti-aging combo.", "recommendation": "Apply peptides first, then retinol.", "scientific_basis": "Peptides signal fibroblasts to produce collagen while retinol upregulates collagen gene expression."},
    {"a": "peptides", "b": "vitamin c", "severity": "neutral", "description": "Generally compatible. Some peptides may be destabilized by very low pH vitamin C serums.", "recommendation": "Fine to use together. If using L-ascorbic acid, apply it first.", "scientific_basis": "Peptide stability depends on pH; most modern formulations are pH-buffered."},
    {"a": "peptides", "b": "niacinamide", "severity": "synergistic", "description": "Niacinamide strengthens the barrier while peptides stimulate collagen. Powerful anti-aging team.", "recommendation": "Use together for maximum anti-aging benefits.", "scientific_basis": "Niacinamide supports barrier function while copper peptides enhance wound healing and collagen synthesis."},
    {"a": "benzoyl peroxide", "b": "retinol", "severity": "avoid", "description": "BPO completely deactivates retinol through oxidation. You get side effects without benefits.", "recommendation": "Use at completely different times. BPO morning, retinol night.", "scientific_basis": "BPO is a peroxide that oxidizes the retinol molecule, rendering it inactive."},
    {"a": "benzoyl peroxide", "b": "vitamin c", "severity": "caution", "description": "BPO can oxidize vitamin C, reducing its antioxidant efficacy.", "recommendation": "Use vitamin C in the morning before BPO, or at night.", "scientific_basis": "Ascorbic acid is easily oxidized by peroxides."},
    {"a": "retinyl palmitate", "b": "glycolic acid", "severity": "avoid", "description": "Even gentle retinyl palmitate combined with glycolic acid causes irritation.", "recommendation": "Use at different times.", "scientific_basis": "Retinyl palmitate converts to retinoic acid; glycolic acid accelerates this conversion too quickly."},
    {"a": "bakuchiol", "b": "retinol", "severity": "caution", "description": "Both stimulate similar pathways. Using both is redundant and may cause irritation.", "recommendation": "Choose one or the other, not both.", "scientific_basis": "Bakuchiol is a natural retinol alternative that works on similar receptors."},
    {"a": "bakuchiol", "b": "vitamin c", "severity": "synergistic", "description": "Bakuchiol provides retinol-like benefits without the irritation, pairing well with vitamin C.", "recommendation": "Bakuchiol at night, vitamin C in the morning.", "scientific_basis": "Bakuchiol is gentle enough to not interfere with vitamin C's efficacy."},
    {"a": "azelaic acid", "b": "vitamin c", "severity": "caution", "description": "Both are effective at different pH ranges. Layering can cause stinging.", "recommendation": "Use at different times for best results.", "scientific_basis": "Azelaic acid works at pH 4-5 while vitamin C needs pH 2.5-3.5."},
    {"a": "azelaic acid", "b": "niacinamide", "severity": "synergistic", "description": "Excellent combination for acne and hyperpigmentation. Both are well-tolerated together.", "recommendation": "Use together for comprehensive brightening and anti-acne.", "scientific_basis": "Azelaic acid kills acne bacteria and reduces keratinization; niacinamide reduces inflammation."},
    {"a": "kojic acid", "b": "vitamin c", "severity": "synergistic", "description": "Both inhibit melanin production through different mechanisms. Powerful brightening combo.", "recommendation": "Use together for maximum brightening effect.", "scientific_basis": "Kojic acid inhibits tyrosinase copper coordination; vitamin C reduces oxidized melanin."},
    {"a": "arbutin", "b": "vitamin c", "severity": "synergistic", "description": "Arbutin blocks melanin production while vitamin C brightens existing spots.", "recommendation": "Apply together for comprehensive hyperpigmentation treatment.", "scientific_basis": "Arbutin is a tyrosinase inhibitor; vitamin C is an antioxidant that reduces melanin."},
    {"a": "tranexamic acid", "b": "niacinamide", "severity": "synergistic", "description": "Both reduce hyperpigmentation through different pathways. Excellent for melasma.", "recommendation": "Use together daily for stubborn pigmentation.", "scientific_basis": "Tranexamic acid inhibits plasmin-mediated melanin synthesis; niacinamide blocks melanosome transfer."},
    {"a": "retinol", "b": "ceramides", "severity": "synergistic", "description": "Ceramides repair the skin barrier that retinol can compromise. Essential pairing.", "recommendation": "Always use ceramides with retinol to minimize irritation.", "scientific_basis": "Retinol disrupts the barrier temporarily; ceramides replenish the lipid matrix."},
    {"a": "retinol", "b": "centella asiatica", "severity": "synergistic", "description": "Centella soothes and repairs retinol-irritated skin while promoting collagen.", "recommendation": "Use centella in the same routine or as a recovery product.", "scientific_basis": "Madecassoside from centella stimulates collagen and reduces inflammation."},
    {"a": "retinol", "b": "squalane", "severity": "synergistic", "description": "Squalane locks in moisture and prevents retinol-induced dryness without clogging pores.", "recommendation": "Apply squalane as a moisturizer over retinol.", "scientific_basis": "Squalane is a lightweight emollient that reinforces the lipid barrier."},
    {"a": "retinol", "b": "alcohol denat", "severity": "avoid", "description": "Denatured alcohol strips the skin of oils, massively amplifying retinol's drying effects.", "recommendation": "Avoid alcohol-containing products when using retinol.", "scientific_basis": "Alcohol disrupts the lipid barrier, and retinol already compromises barrier function."},
    {"a": "aha", "b": "bha", "severity": "caution", "description": "Using both acids together can lead to over-exfoliation and sensitized skin.", "recommendation": "Use BHA for pores in the morning, AHA for surface at night, or alternate days.", "scientific_basis": "Different exfoliation depths combined can be too aggressive."},
    {"a": "salicylic acid", "b": "retinol", "severity": "avoid", "description": "Double exfoliation from BHA and retinol damages the skin barrier.", "recommendation": "Alternate days or use at different times.", "scientific_basis": "Both increase cell turnover through different mechanisms."},
    {"a": "vitamin e", "b": "retinol", "severity": "synergistic", "description": "Vitamin E stabilizes retinol and provides additional antioxidant protection.", "recommendation": "Great combination for anti-aging routines.", "scientific_basis": "Vitamin E protects retinol from oxidation and enhances its photoprotective effects."},
    {"a": "ceramides", "b": "niacinamide", "severity": "synergistic", "description": "Niacinamide boosts ceramide production naturally, enhancing the barrier repair.", "recommendation": "Perfect barrier-repair combination.", "scientific_basis": "Niacinamide upregulates ceramide synthase, increasing endogenous ceramide production."},
    {"a": "ceramides", "b": "hyaluronic acid", "severity": "synergistic", "description": "HA hydrates while ceramides seal moisture in. The foundation of any moisturizer.", "recommendation": "Look for products containing both, or layer HA under ceramide cream.", "scientific_basis": "HA provides water-binding capacity; ceramides prevent water loss through the lipid barrier."},
    {"a": "centella asiatica", "b": "retinol", "severity": "synergistic", "description": "Centella soothes and repairs retinol-irritated skin.", "recommendation": "Use centella serum alongside retinol for better tolerance.", "scientific_basis": "Madecassoside reduces inflammation and stimulates collagen synthesis."},
    {"a": "centella asiatica", "b": "vitamin c", "severity": "synergistic", "description": "Centella calms and repairs while vitamin C brightens and protects.", "recommendation": "Layer centella under vitamin C.", "scientific_basis": "Centella's anti-inflammatory action complements vitamin C's antioxidant protection."},
    {"a": "green tea", "b": "vitamin c", "severity": "synergistic", "description": "Green tea EGCG and vitamin C together provide enhanced antioxidant protection.", "recommendation": "Excellent antioxidant combination for morning routines.", "scientific_basis": "EGCG scavenges free radicals while vitamin C neutralizes ROS through different mechanisms."},
    {"a": "green tea", "b": "retinol", "severity": "synergistic", "description": "Green tea's anti-inflammatory properties help offset retinol irritation.", "recommendation": "Use green tea serum with retinol for better tolerance.", "scientific_basis": "EGCG reduces MMP expression and inflammation caused by retinoids."},
    {"a": "tea tree oil", "b": "retinol", "severity": "caution", "description": "Tea tree oil is a potential irritant that can compound retinol's irritation.", "recommendation": "Use tea tree as spot treatment, not all over with retinol.", "scientific_basis": "Terpenes in tea tree oil can disrupt the barrier, adding to retinol's effects."},
    {"a": "tea tree oil", "b": "aha", "severity": "caution", "description": "Both can irritate sensitive skin. Combined use may cause redness.", "recommendation": "Use at different times.", "scientific_basis": "Tea tree oil's antimicrobial action plus AHA's exfoliation can overwhelm sensitive skin."},
    {"a": "retinol", "b": "witch hazel", "severity": "avoid", "description": "Witch hazel (alcohol-based) is astringent and severely dehydrates skin already stressed by retinol.", "recommendation": "Replace witch hazel with a gentle toner when using retinol.", "scientific_basis": "Tannins and alcohol in witch hazel strip lipids that retinol-dependent skin needs."},
    {"a": "vitamin c", "b": "chemical sunscreen", "severity": "synergistic", "description": "Vitamin C enhances sunscreen's UV protection by neutralizing free radicals that slip through.", "recommendation": "Always pair vitamin C with broad-spectrum SPF.", "scientific_basis": "Vitamin C provides a second line of defense against UV-generated ROS."},
    {"a": "retinol", "b": "chemical sunscreen", "severity": "synergistic", "description": "Retinol increases photosensitivity. SPF is absolutely essential.", "recommendation": "Never skip sunscreen when using retinol.", "scientific_basis": "Retinol thins the stratum corneum, reducing natural UV defense."},
    {"a": "clay", "b": "retinol", "severity": "caution", "description": "Clay masks absorb oils that retinol-treated skin needs. Can cause extreme dryness.", "recommendation": "Limit clay masks to once a week and moisturize well after.", "scientific_basis": "Clay absorbs sebum, which is already reduced by retinol."},
    {"a": "clay", "b": "aha", "severity": "caution", "description": "Clay + AHA mask can cause over-exfoliation and irritation.", "recommendation": "Use clay in the morning, AHA at night.", "scientific_basis": "Clay increases skin permeability while AHA penetrates more aggressively."},
    {"a": "charcoal", "b": "retinol", "severity": "caution", "description": "Charcoal draws out oils that retinol-treated skin needs for barrier function.", "recommendation": "Use charcoal products sparingly with retinol.", "scientific_basis": "Activated charcoal adsorbs lipids, potentially weakening the retinol-compromised barrier."},
    {"a": "retinol", "b": "allantoin", "severity": "synergistic", "description": "Allantoin soothes and protects retinol-irritated skin while promoting cell regeneration.", "recommendation": "Look for moisturizers containing allantoin when using retinol.", "scientific_basis": "Allantoin is a keratolytic that softens keratin and promotes cell proliferation."},
    {"a": "retinol", "b": "panthenol", "severity": "synergistic", "description": "Panthenol (vitamin B5) deeply moisturizes and heals retinol-irritated skin.", "recommendation": "Apply panthenol-rich products alongside retinol routines.", "scientific_basis": "Panthenol converts to pantothenic acid, which is essential for coenzyme A in skin barrier lipids."},
    {"a": "retinol", "b": "urea", "severity": "caution", "description": "Urea at high concentrations (>10%) can increase retinol penetration too much.", "recommendation": "Use low-concentration urea (2-5%) with retinol.", "scientific_basis": "Urea at high concentrations is a penetration enhancer that can amplify retinol's effects."},
    {"a": "niacinamide", "b": "retinol", "severity": "synergistic", "description": "Niacinamide reduces retinol irritation while providing its own anti-aging benefits.", "recommendation": "Excellent combination. Use niacinamide with or before retinol.", "scientific_basis": "Niacinamide upregulates ceramide synthesis, offsetting retinol's barrier disruption."},
    {"a": "zinc oxide", "b": "retinol", "severity": "synergistic", "description": "Mineral sunscreen with zinc oxide protects retinol-sensitized skin from UV.", "recommendation": "Use zinc oxide sunscreen daily with retinol.", "scientific_basis": "Zinc oxide provides broad-spectrum physical UV protection without chemical irritation."},
]

# Build lookup index
_INTERACTION_INDEX: Dict[tuple, Dict] = {}
for ix in INTERACTIONS_DB:
    key_a = ix["a"].lower().strip()
    key_b = ix["b"].lower().strip()
    _INTERACTION_INDEX[(key_a, key_b)] = ix
    _INTERACTION_INDEX[(key_b, key_a)] = ix


INGREDIENT_DB: List[Dict[str, Any]] = [
    {"name": "Retinol", "category": "active", "description": "Vitamin A derivative that accelerates cell turnover and collagen production.", "pairs_well_with": ["hyaluronic acid", "ceramides", "centella asiatica", "squalane", "panthenol", "niacinamide", "zinc oxide"], "avoid_with": ["glycolic acid", "lactic acid", "salicylic acid", "benzoyl peroxide", "aha", "bha", "alcohol denat", "witch hazel"], "safety_level": "actives_caution"},
    {"name": "Vitamin C", "category": "antioxidant", "description": "Powerful antioxidant that brightens skin, boosts collagen, and protects against free radicals.", "pairs_well_with": ["hyaluronic acid", "vitamin e", "ferulic acid", "niacinamide", "kojic acid", "arbutin", "green tea"], "avoid_with": ["glycolic acid", "aha"], "safety_level": "actives_caution"},
    {"name": "Niacinamide", "category": "active", "description": "Vitamin B3 that strengthens the skin barrier, reduces pores, and controls oil.", "pairs_well_with": ["hyaluronic acid", "retinol", "vitamin c", "ceramides", "tranexamic acid", "azelaic acid", "peptides"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Hyaluronic Acid", "category": "hydrating", "description": "Humectant that holds 1000x its weight in water, plumping and hydrating skin.", "pairs_well_with": ["retinol", "vitamin c", "niacinamide", "peptides", "ceramides", "squalane", "glycolic acid", "vitamin e"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Glycolic Acid", "category": "exfoliant", "description": "AHA that exfoliates the skin surface, improves texture, and boosts cell turnover.", "pairs_well_with": ["hyaluronic acid", "centella asiatica"], "avoid_with": ["retinol", "vitamin c", "aha", "retinyl palmitate"], "safety_level": "actives_caution"},
    {"name": "Lactic Acid", "category": "exfoliant", "description": "Gentle AHA that exfoliates and hydrates simultaneously.", "pairs_well_with": ["hyaluronic acid", "centella asiatica", "ceramides"], "avoid_with": ["retinol", "vitamin c", "aha"], "safety_level": "actives_caution"},
    {"name": "Salicylic Acid", "category": "exfoliant", "description": "BHA that penetrates pores to clear congestion and reduce acne.", "pairs_well_with": ["hyaluronic acid", "green tea"], "avoid_with": ["retinol", "retinol", "benzoyl peroxide", "retinol"], "safety_level": "actives_caution"},
    {"name": "Benzoyl Peroxide", "category": "active", "description": "Antibacterial that kills acne-causing bacteria. Effective but can be drying.", "pairs_well_with": ["hyaluronic acid", "ceramides", "centella asiatica"], "avoid_with": ["retinol", "vitamin c", "retinol"], "safety_level": "actives_caution"},
    {"name": "Vitamin E", "category": "antioxidant", "description": "Fat-soluble antioxidant that protects cell membranes and enhances other antioxidants.", "pairs_well_with": ["vitamin c", "ferulic acid", "hyaluronic acid", "retinol", "squalane"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Ceramides", "category": "emollient", "description": "Lipids that form the skin barrier, preventing moisture loss and protecting against irritants.", "pairs_well_with": ["hyaluronic acid", "niacinamide", "retinol", "squalane", "centella asiatica", "panthenol"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Peptides", "category": "active", "description": "Amino acid chains that signal skin to produce more collagen and elastin.", "pairs_well_with": ["hyaluronic acid", "retinol", "niacinamide", "ceramides", "vitamin e"], "avoid_with": ["aha", "bha"], "safety_level": "actives_caution"},
    {"name": "AHA", "category": "exfoliant", "description": "Alpha Hydroxy Acid - umbrella term for glycolic, lactic, mandelic acids.", "pairs_well_with": ["hyaluronic acid", "centella asiatica"], "avoid_with": ["retinol", "vitamin c", "bha", "peptides", "niacinamide"], "safety_level": "actives_caution"},
    {"name": "BHA", "category": "exfoliant", "description": "Beta Hydroxy Acid - oil-soluble exfoliant that clears pores.", "pairs_well_with": ["hyaluronic acid", "green tea"], "avoid_with": ["retinol", "retinol", "peptides", "retinol"], "safety_level": "actives_caution"},
    {"name": "Ferulic Acid", "category": "antioxidant", "description": "Plant-based antioxidant that stabilizes vitamins C and E.", "pairs_well_with": ["vitamin c", "vitamin e"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Centella Asiatica", "category": "active", "description": "CICA - soothing herb that repairs skin and stimulates collagen.", "pairs_well_with": ["retinol", "vitamin c", "ceramides", "hyaluronic acid", "niacinamide"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Kojic Acid", "category": "active", "description": "Mushroom-derived brightening agent that inhibits melanin production.", "pairs_well_with": ["vitamin c", "arbutin", "niacinamide"], "avoid_with": ["aha", "glycolic acid"], "safety_level": "sensitive_caution"},
    {"name": "Arbutin", "category": "active", "description": "Natural brightening agent derived from bearberry that blocks melanin.", "pairs_well_with": ["vitamin c", "niacinamide", "kojic acid"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Tranexamic Acid", "category": "active", "description": "Anti-inflammatory brightening agent effective for melasma and dark spots.", "pairs_well_with": ["niacinamide", "vitamin c", "arbutin"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Azelaic Acid", "category": "active", "description": "Multi-tasker that fights acne, reduces redness, and brightens skin.", "pairs_well_with": ["niacinamide", "hyaluronic acid", "retinol"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Bakuchiol", "category": "active", "description": "Natural retinol alternative from babchi plant. Gentle enough for sensitive skin.", "pairs_well_with": ["vitamin c", "hyaluronic acid", "niacinamide", "ceramides"], "avoid_with": ["retinol"], "safety_level": "safe_for_most"},
    {"name": "Squalane", "category": "emollient", "description": "Lightweight plant-derived oil that mimics skin's natural sebum.", "pairs_well_with": ["retinol", "hyaluronic acid", "vitamin c", "ceramides", "peptides"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Green Tea", "category": "antioxidant", "description": "Rich in EGCG antioxidants that reduce inflammation and protect against UV damage.", "pairs_well_with": ["vitamin c", "retinol", "hyaluronic acid", "niacinamide"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Tea Tree Oil", "category": "active", "description": "Natural antibacterial and anti-inflammatory essential oil for acne.", "pairs_well_with": ["hyaluronic acid", "niacinamide"], "avoid_with": ["retinol", "aha", "glycolic acid"], "safety_level": "sensitive_caution"},
    {"name": "Witch Hazel", "category": "astringent", "description": "Natural astringent that can tighten pores but may be drying.", "pairs_well_with": ["hyaluronic acid", "ceramides"], "avoid_with": ["retinol", "aha", "bha"], "safety_level": "sensitive_caution"},
    {"name": "Alcohol Denat", "category": "solvent", "description": "Drying alcohol used as a solvent. Can be very stripping.", "pairs_well_with": [], "avoid_with": ["retinol", "aha", "bha", "retinol"], "safety_level": "sensitive_caution"},
    {"name": "Clay", "category": "absorbent", "description": "Kaolin/bentonite clay that absorbs excess oil and impurities.", "pairs_well_with": ["hyaluronic acid", "ceramides", "green tea"], "avoid_with": ["retinol", "aha"], "safety_level": "sensitive_caution"},
    {"name": "Charcoal", "category": "absorbent", "description": "Activated charcoal that draws out impurities and excess oil.", "pairs_well_with": ["hyaluronic acid", "ceramides"], "avoid_with": ["retinol"], "safety_level": "sensitive_caution"},
    {"name": "Panthenol", "category": "hydrating", "description": "Vitamin B5 that deeply moisturizes, soothes, and promotes healing.", "pairs_well_with": ["retinol", "hyaluronic acid", "ceramides", "niacinamide", "centella asiatica"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Allantoin", "category": "hydrating", "description": "Soothing compound that promotes cell regeneration and healing.", "pairs_well_with": ["retinol", "hyaluronic acid", "ceramides", "panthenol"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Urea", "category": "hydrating", "description": "Natural moisturizing factor that softens skin and boosts hydration.", "pairs_well_with": ["hyaluronic acid", "ceramides", "niacinamide"], "avoid_with": ["retinol"], "safety_level": "sensitive_caution"},
    {"name": "Collagen", "category": "emollient", "description": "Protein that provides structural support. Topical collagen hydrates but doesn't penetrate.", "pairs_well_with": ["hyaluronic acid", "vitamin c", "peptides", "ceramides"], "avoid_with": [], "safety_level": "safe_for_most"},
    {"name": "Mandelic Acid", "category": "exfoliant", "description": "Gentle AHA derived from almonds. Larger molecule = less irritation.", "pairs_well_with": ["hyaluronic acid", "niacinamide", "centella asiatica"], "avoid_with": ["retinol", "aha", "bha"], "safety_level": "actives_caution"},
    {"name": "PHA", "category": "exfoliant", "description": "Polyhydroxy Acid - gentle exfoliant with humectant properties.", "pairs_well_with": ["hyaluronic acid", "niacinamide", "retinol"], "avoid_with": ["aha", "bha"], "safety_level": "safe_for_most"},
]


# ── Pydantic Schemas ────────────────────────────────────────────────

class InteractionCheckRequest(BaseModel):
    ingredients: List[str] = Field(..., min_length=2, max_length=10, description="List of 2-10 ingredient names")

class InteractionPair(BaseModel):
    ingredient_a: str
    ingredient_b: str
    severity: str
    description: str
    recommendation: str
    scientific_basis: str

class InteractionCheckResponse(BaseModel):
    interactions: List[InteractionPair]
    overall_safety: str
    safety_score: float
    routine_tip: str
    conflicts_count: int
    synergies_count: int
    safe_count: int

class IngredientSearchResult(BaseModel):
    name: str
    category: str
    description: str
    pairs_well_with: List[str]
    avoid_with: List[str]
    safety_level: str

class PopularCombination(BaseModel):
    name: str
    ingredients: List[str]
    safety: str
    description: str

class RoutineProduct(BaseModel):
    name: str
    ingredients: List[str]

class RoutineAnalysisRequest(BaseModel):
    products: List[RoutineProduct] = Field(..., min_length=2, max_length=10)

class ProductPairInteraction(BaseModel):
    product_a: str
    product_b: str
    conflicting_ingredients: List[str]
    severity: str
    description: str

class RoutineAnalysisResponse(BaseModel):
    product_interactions: List[ProductPairInteraction]
    overall_routine_safety: str
    safety_score: float
    recommendations: List[str]


# ── Helper Functions ────────────────────────────────────────────────

def _normalize(name: str) -> str:
    n = name.lower().strip()
    aliases = {
        "vitamin c": "vitamin c", "l-ascorbic acid": "vitamin c", "ascorbic acid": "vitamin c", "sodium ascorbyl phosphate": "vitamin c", "magnesium ascorbyl phosphate": "vitamin c",
        "retinol": "retinol", "retinal": "retinol", "tretinoin": "retinol", "retinoic acid": "retinol", "adapalene": "retinol", "retinyl palmitate": "retinol",
        "niacinamide": "niacinamide", "vitamin b3": "niacinamide", "nicotinamide": "niacinamide",
        "hyaluronic acid": "hyaluronic acid", "ha": "hyaluronic acid", "sodium hyaluronate": "hyaluronic acid", "hyaluronate": "hyaluronic acid",
        "glycolic acid": "glycolic acid", "aha": "aha", "lactic acid": "lactic acid", "mandelic acid": "mandelic acid", "pha": "pha",
        "salicylic acid": "salicylic acid", "bha": "bha",
        "benzoyl peroxide": "benzoyl peroxide", "bpo": "benzoyl peroxide",
        "ceramides": "ceramides", "ceramide": "ceramides",
        "peptides": "peptides", "peptide": "peptides", "copper peptides": "peptides",
        "azelaic acid": "azelaic acid",
        "kojic acid": "kojic acid",
        "arbutin": "arbutin", "alpha arbutin": "arbutin", "beta arbutin": "arbutin",
        "tranexamic acid": "tranexamic acid",
        "bakuchiol": "bakuchiol",
        "squalane": "squalane", "squalene": "squalane",
        "centella asiatica": "centella asiatica", "cica": "centella asiatica", "madecassoside": "centella asiatica",
        "green tea": "green tea", "egcg": "green tea",
        "tea tree oil": "tea tree oil", "melaleuca": "tea tree oil",
        "witch hazel": "witch hazel",
        "alcohol denat": "alcohol denat",
        "clay": "clay", "kaolin": "clay", "bentonite": "clay",
        "charcoal": "charcoal", "activated charcoal": "charcoal",
        "vitamin e": "vitamin e", "tocopherol": "vitamin e",
        "ferulic acid": "ferulic acid",
        "panthenol": "panthenol", "vitamin b5": "panthenol", "pro-vitamin b5": "panthenol",
        "allantoin": "allantoin",
        "urea": "urea",
        "collagen": "collagen",
        "retinyl palmitate": "retinyl palmitate",
    }
    return aliases.get(n, n)


def _find_interactions(ingredients: List[str]) -> List[InteractionPair]:
    found = []
    seen = set()
    normalized = [_normalize(i) for i in ingredients]
    for i in range(len(normalized)):
        for j in range(i + 1, len(normalized)):
            key = (normalized[i], normalized[j])
            key_rev = (normalized[j], normalized[i])
            if key in seen or key_rev in seen:
                continue
            seen.add(key)
            ix = _INTERACTION_INDEX.get(key) or _INTERACTION_INDEX.get(key_rev)
            if ix:
                found.append(InteractionPair(
                    ingredient_a=ingredients[i].strip().title(),
                    ingredient_b=ingredients[j].strip().title(),
                    severity=ix["severity"],
                    description=ix["description"],
                    recommendation=ix["recommendation"],
                    scientific_basis=ix["scientific_basis"],
                ))
    return found


def _compute_safety(interactions: List[InteractionPair]) -> tuple:
    if not interactions:
        return 100.0, "safe", "All ingredients in this combination are compatible!"
    severity_weights = {"avoid": 30, "caution": 12, "neutral": 0, "synergistic": -8}
    penalty = sum(severity_weights.get(ix.severity, 0) for ix in interactions)
    score = max(0, min(100, 100 - penalty))
    conflicts = sum(1 for ix in interactions if ix.severity == "avoid")
    synergies = sum(1 for ix in interactions if ix.severity == "synergistic")
    cautions = sum(1 for ix in interactions if ix.severity == "caution")
    if conflicts > 0:
        safety = "avoid_mix"
        tip = f"Warning: {conflicts} dangerous combination(s) found. Separate these ingredients into AM/PM routines."
    elif cautions > 0:
        safety = "cautions"
        tip = f"Use with caution: {cautions} potentially irritating combination(s). Consider using at different times."
    else:
        safety = "safe"
        tip = "Great combination! These ingredients work well together."
    if synergies > len(interactions) // 2:
        tip += f" Plus, {synergies} synergistic pairs boost each other's efficacy!"
    return score, safety, tip


# ── Endpoints ───────────────────────────────────────────────────────

@router.post("/check", response_model=InteractionCheckResponse)
async def check_interactions(body: InteractionCheckRequest):
    ingredients = [i.strip() for i in body.ingredients if i.strip()]
    if len(ingredients) < 2:
        raise HTTPException(status_code=400, detail="At least 2 ingredients required")
    interactions = _find_interactions(ingredients)
    score, safety, tip = _compute_safety(interactions)
    return InteractionCheckResponse(
        interactions=interactions,
        overall_safety=safety,
        safety_score=score,
        routine_tip=tip,
        conflicts_count=sum(1 for ix in interactions if ix.severity == "avoid"),
        synergies_count=sum(1 for ix in interactions if ix.severity == "synergistic"),
        safe_count=sum(1 for ix in interactions if ix.severity in ("neutral", "synergistic")),
    )


@router.get("/popular", response_model=List[PopularCombination])
async def get_popular():
    return [
        PopularCombination(name="Anti-Aging Night Routine", ingredients=["Retinol", "Hyaluronic Acid", "Ceramides", "Niacinamide"], safety="safe", description="The gold standard anti-aging routine. Retinol accelerates turnover while HA and ceramides protect the barrier."),
        PopularCombination(name="Brightening Power Combo", ingredients=["Vitamin C", "Niacinamide", "Arbutin", "Hyaluronic Acid"], safety="safe", description="Maximum brightening through multiple melanin-blocking pathways."),
        PopularCombination(name="Acne Fighter Stack", ingredients=["Salicylic Acid", "Niacinamide", "Azelaic Acid", "Hyaluronic Acid"], safety="cautions", description="Multi-pronged approach to acne. BHA clears pores, niacinamide controls oil, azelaic acid kills bacteria."),
        PopularCombination(name="Retinol + Vitamin C (Split)", ingredients=["Retinol", "Vitamin C", "Hyaluronic Acid", "Ceramides"], safety="cautions", description="Use Vitamin C in AM, Retinol in PM. Both are potent actives that work best separately."),
        PopularCombination(name="Sensitive Skin Safe Routine", ingredients=["Centella Asiatica", "Ceramides", "Panthenol", "Hyaluronic Acid"], safety="safe", description="Gentle, calming routine for reactive skin. All ingredients are well-tolerated."),
        PopularCombination(name="Dark Spot Corrector", ingredients=["Tranexamic Acid", "Vitamin C", "Kojic Acid", "Niacinamide"], safety="cautions", description="Aggressive brightening routine. Use carefully and always wear SPF."),
        PopularCombination(name="Anti-Aging Morning", ingredients=["Vitamin C", "Vitamin E", "Ferulic Acid", "Hyaluronic Acid", "Ceramides"], safety="safe", description="The C+E+Ferulic trio provides 8x photoprotection. The gold standard antioxidant morning routine."),
        PopularCombination(name="Acne + Anti-Aging", ingredients=["Niacinamide", "Azelaic Acid", "Peptides", "Hyaluronic Acid"], safety="safe", description="Address acne and aging simultaneously without irritation."),
        PopularCombination(name="Oily Skin Control", ingredients=["Salicylic Acid", "Niacinamide", "Green Tea", "Hyaluronic Acid"], safety="cautions", description="Controls excess oil while keeping skin hydrated. BHA morning, niacinamide night."),
        PopularCombination(name="Barrier Repair", ingredients=["Ceramides", "Niacinamide", "Hyaluronic Acid", "Panthenol", "Centella Asiatica"], safety="safe", description="Maximum barrier repair combo. Ideal for post-procedure or compromised skin."),
    ]


@router.get("/encyclopedia")
async def get_encyclopedia():
    avoid = [{"a": ix["a"].title(), "b": ix["b"].title(), "description": ix["description"], "recommendation": ix["recommendation"]} for ix in INTERACTIONS_DB if ix["severity"] == "avoid"]
    caution = [{"a": ix["a"].title(), "b": ix["b"].title(), "description": ix["description"], "recommendation": ix["recommendation"]} for ix in INTERACTIONS_DB if ix["severity"] == "caution"]
    synergistic = [{"a": ix["a"].title(), "b": ix["b"].title(), "description": ix["description"], "recommendation": ix["recommendation"]} for ix in INTERACTIONS_DB if ix["severity"] == "synergistic"]
    return {"avoid": avoid, "caution": caution, "synergistic": synergistic, "total_interactions": len(INTERACTIONS_DB)}


@router.post("/analyze-routine", response_model=RoutineAnalysisResponse)
async def analyze_routine(body: RoutineAnalysisRequest):
    all_interactions: List[ProductPairInteraction] = []
    for i in range(len(body.products)):
        for j in range(i + 1, len(body.products)):
            p_a = body.products[i]
            p_b = body.products[j]
            conflicts = []
            worst = "safe"
            severity_order = {"safe": 0, "neutral": 0, "synergistic": 1, "caution": 2, "avoid": 3}
            for ing_a in p_a.ingredients:
                for ing_b in p_b.ingredients:
                    n_a = _normalize(ing_a)
                    n_b = _normalize(ing_b)
                    ix = _INTERACTION_INDEX.get((n_a, n_b)) or _INTERACTION_INDEX.get((n_b, n_a))
                    if ix and ix["severity"] in ("avoid", "caution"):
                        conflicts.append(f"{ing_a} + {ing_b}")
                        if severity_order.get(ix["severity"], 0) > severity_order.get(worst, 0):
                            worst = ix["severity"]
            if conflicts:
                all_interactions.append(ProductPairInteraction(
                    product_a=p_a.name,
                    product_b=p_b.name,
                    conflicting_ingredients=conflicts,
                    severity=worst,
                    description=f"{len(conflicts)} conflicting ingredient pair(s) found between {p_a.name} and {p_b.name}.",
                ))
    avoid_count = sum(1 for pi in all_interactions if pi.severity == "avoid")
    caution_count = sum(1 for pi in all_interactions if pi.severity == "caution")
    total_pairs = len(body.products) * (len(body.products) - 1) // 2
    safe_pairs = total_pairs - len(all_interactions)
    score = max(0, min(100, 100 - (avoid_count * 30) - (caution_count * 12)))
    if avoid_count > 0:
        safety = "avoid_mix"
    elif caution_count > 0:
        safety = "cautions"
    else:
        safety = "safe"
    recs = []
    if avoid_count:
        recs.append(f"Remove or separate {avoid_count} conflicting product pair(s) into AM/PM routines.")
    if caution_count:
        recs.append(f"Use {caution_count} caution-level pair(s) at different times of day.")
    if not all_interactions:
        recs.append("Your routine has no ingredient conflicts! All products are compatible.")
    else:
        recs.append(f"{safe_pairs} out of {total_pairs} product pairs have no conflicts.")
    return RoutineAnalysisResponse(
        product_interactions=all_interactions,
        overall_routine_safety=safety,
        safety_score=score,
        recommendations=recs,
    )


@router.get("/ingredients/search/{query}", response_model=List[IngredientSearchResult])
async def search_ingredients(query: str):
    q = query.lower().strip()
    if len(q) < 1:
        return []
    results = []
    seen = set()
    for ing in INGREDIENT_DB:
        name_lower = ing["name"].lower()
        if q in name_lower or q in ing["description"].lower():
            if ing["name"] not in seen:
                seen.add(ing["name"])
                results.append(IngredientSearchResult(**ing))
    if not results:
        for ing in INGREDIENT_DB:
            name_lower = ing["name"].lower()
            if any(word in name_lower for word in q.split()):
                if ing["name"] not in seen:
                    seen.add(ing["name"])
                    results.append(IngredientSearchResult(**ing))
    return results[:15]
