from fastapi import APIRouter, HTTPException
from app.schemas.astro import BirthDataRequest, AstroResponse
from app.services.astro_service import astro_service

router = APIRouter()

@router.post("/birth-chart", response_model=AstroResponse)
async def get_birth_chart(birth_data: BirthDataRequest):
    """
    Get birth chart data from Astro API
    """
    try:
        chart_data = await astro_service.get_birth_chart(birth_data)
        if not chart_data:
            raise HTTPException(status_code=400, detail="Unable to generate birth chart")
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating birth chart: {str(e)}")

@router.get("/health")
async def astro_health():
    """Health check for astro service"""
    return {"status": "healthy", "service": "astro-api"}