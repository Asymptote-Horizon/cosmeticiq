from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.schemas import ClaimAnalysisRequest, ClaimAnalysisResponse
from app.ai.rag_service import rag_service

router = APIRouter(prefix="/claims", tags=["Claims Verification"])


@router.post("/analyze", response_model=ClaimAnalysisResponse)
async def analyze_claim(request: ClaimAnalysisRequest):
    """Analyze an influencer claim against scientific evidence."""
    
    # Use RAG to verify the claim
    if request.product_name:
        result = await rag_service.verify_claim(request.content, request.product_name)
    else:
        result = await rag_service.verify_claim(request.content, "general")
    
    # Generate explanation based on verdict
    explanations = {
        "supported": "This claim is supported by scientific evidence. Multiple research studies confirm the benefits mentioned.",
        "partially_supported": "This claim has some scientific backing, but the evidence is not conclusive. Some aspects may be exaggerated.",
        "misleading": "This claim is not fully supported by scientific evidence. The benefits mentioned may be overstated or inaccurate.",
        "no_evidence": "No scientific evidence was found to support this claim. Consider this as marketing rather than fact."
    }
    
    return ClaimAnalysisResponse(
        verdict=result["verdict"],
        confidence_score=result["confidence"],
        evidence=result["evidence"],
        explanation=explanations.get(result["verdict"], "Unable to verify this claim."),
        scientific_references=result["evidence"]
    )


@router.post("/batch-analyze")
async def batch_analyze_claims(claims: List[ClaimAnalysisRequest]):
    """Analyze multiple claims at once."""
    results = []
    for claim in claims:
        result = await analyze_claim(claim)
        results.append(result)
    return {"results": results, "count": len(results)}
