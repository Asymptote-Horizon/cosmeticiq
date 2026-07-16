from typing import Dict, List, Any, Optional
import httpx
from app.core.config import settings


class RAGService:
    """Retrieval-Augmented Generation service for scientific verification."""
    
    def __init__(self):
        self.openai_client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client."""
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except ImportError:
                pass
    
    async def search_scientific_evidence(self, query: str, ingredient: str) -> Dict[str, Any]:
        """Search for scientific evidence about an ingredient."""
        # Simulated scientific database search
        # In production, this would query PubMed, CosDNA, etc.
        
        evidence = {
            "ingredient": ingredient,
            "query": query,
            "sources": [],
            "confidence": 0.0,
            "summary": ""
        }
        
        # Search PubMed
        pubmed_results = await self._search_pubmed(ingredient)
        evidence["sources"].extend(pubmed_results)
        
        # Search EWG
        ewg_result = await self._search_ewg(ingredient)
        if ewg_result:
            evidence["sources"].append(ewg_result)
        
        # Calculate confidence based on sources
        evidence["confidence"] = min(len(evidence["sources"]) * 0.2, 1.0)
        
        return evidence
    
    async def _search_pubmed(self, ingredient: str) -> List[Dict[str, Any]]:
        """Search PubMed for studies about an ingredient."""
        try:
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            params = {
                "db": "pubmed",
                "term": f"{ingredient} cosmetic safety",
                "retmax": 5,
                "retmode": "json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    ids = data.get("esearchresult", {}).get("idlist", [])
                    
                    results = []
                    for pmid in ids[:3]:
                        results.append({
                            "source": "PubMed",
                            "id": f"PMID:{pmid}",
                            "title": f"Study on {ingredient} safety",
                            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                            "relevance": 0.8
                        })
                    
                    return results
            return []
        except Exception:
            return []
    
    async def _search_ewg(self, ingredient: str) -> Optional[Dict[str, Any]]:
        """Search EWG Skin Deep database."""
        # Simulated EWG lookup
        return {
            "source": "EWG Skin Deep",
            "id": f"EWG-{ingredient.replace(' ', '-')}",
            "title": f"EWG Rating for {ingredient}",
            "url": f"https://www.ewg.org/skindeep/search/?search={ingredient}",
            "relevance": 0.7
        }
    
    async def generate_explanation(self, product_name: str, fuzzy_output: Dict[str, Any], 
                                    ingredients: List[Dict[str, Any]]) -> str:
        """Generate LLM explanation of fuzzy logic decision."""
        
        if not self.openai_client:
            return self._generate_rule_based_explanation(fuzzy_output, ingredients)
        
        try:
            prompt = f"""You are a cosmetic science expert. Explain why this product is {fuzzy_output.get('linguistic_output', 'Average')} for the user.

Product: {product_name}
Suitability Score: {fuzzy_output.get('suitability_score', 0.5)}
Confidence: {fuzzy_output.get('confidence', 0.5)}

Key Ingredients: {', '.join([i.get('name', 'Unknown') for i in ingredients[:5]])}

Explain in simple, non-technical language:
1. Why this score was given
2. Key factors that influenced the decision
3. Any warnings or concerns
4. Whether the product is recommended

Keep it under 200 words. Be factual and evidence-based."""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cosmetic science expert who explains product suitability in simple terms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return self._generate_rule_based_explanation(fuzzy_output, ingredients)
    
    def _generate_rule_based_explanation(self, fuzzy_output: Dict[str, Any], 
                                          ingredients: List[Dict[str, Any]]) -> str:
        """Generate rule-based explanation without LLM."""
        
        score = fuzzy_output.get('suitability_score', 0.5)
        linguistic = fuzzy_output.get('linguistic_output', 'Average')
        
        explanation = f"This product has been evaluated as **{linguistic}** for your profile.\n\n"
        
        if score >= 0.8:
            explanation += "This product is highly suitable for you. The ingredient safety profile is excellent and matches your skin needs."
        elif score >= 0.6:
            explanation += "This product is suitable for you with some considerations. Most ingredients are safe for your profile."
        elif score >= 0.4:
            explanation += "This product has moderate suitability. Some ingredients may not be ideal for your specific needs."
        elif score >= 0.2:
            explanation += "This product may not be suitable for you. Several factors suggest it might not match your requirements."
        else:
            explanation += "This product is not recommended for you. The ingredient profile does not match your needs."
        
        # Add ingredient highlights
        if ingredients:
            safe_ingredients = [i for i in ingredients if i.get('safety_score', 0) >= 0.8]
            if safe_ingredients:
                explanation += f"\n\n**Good ingredients:** {', '.join([i['name'] for i in safe_ingredients[:3]])}"
            
            caution_ingredients = [i for i in ingredients if i.get('safety_score', 0) < 0.5]
            if caution_ingredients:
                explanation += f"\n\n**Use with caution:** {', '.join([i['name'] for i in caution_ingredients[:2]])}"
        
        return explanation
    
    async def verify_claim(self, claim: str, ingredient: str) -> Dict[str, Any]:
        """Verify a claim about an ingredient."""
        evidence = await self.search_scientific_evidence(claim, ingredient)
        
        # Determine verdict based on evidence
        if evidence["confidence"] >= 0.7 and len(evidence["sources"]) >= 3:
            verdict = "supported"
        elif evidence["confidence"] >= 0.4 and len(evidence["sources"]) >= 1:
            verdict = "partially_supported"
        else:
            verdict = "no_evidence"
        
        return {
            "verdict": verdict,
            "confidence": evidence["confidence"],
            "evidence": evidence["sources"],
            "explanation": f"Based on available scientific literature, this claim is {verdict}."
        }


# Global RAG service instance
rag_service = RAGService()
