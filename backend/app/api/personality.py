from fastapi import APIRouter, HTTPException
from app.schemas.astro import BirthDataRequest
from app.schemas.personality import PersonalityAssessment, PersonalityTestType
from app.services.astro_service import astro_service
from app.services.personality_engine import personality_engine

router = APIRouter()

@router.post("/full-assessment", response_model=PersonalityAssessment)
async def generate_full_assessment(birth_data: BirthDataRequest):
    """
    Generate complete personality assessment from birth data
    """
    try:
        # Get birth chart from astro service
        astro_data = await astro_service.get_birth_chart(birth_data)
        if not astro_data:
            raise HTTPException(status_code=400, detail="Unable to get astrological data")
        
        # Generate all personality assessments
        assessment = personality_engine.generate_all_assessments(astro_data.birth_chart)
        assessment.user_id = f"user_{birth_data.name.replace(' ', '_').lower()}"
        
        return assessment
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating assessment: {str(e)}")

@router.post("/assessment/{test_type}")
async def generate_single_assessment(test_type: PersonalityTestType, birth_data: BirthDataRequest):
    """
    Generate a single personality test result
    """
    try:
        # Get birth chart
        astro_data = await astro_service.get_birth_chart(birth_data)
        if not astro_data:
            raise HTTPException(status_code=400, detail="Unable to get astrological data")
        
        # Generate full assessment first
        full_assessment = personality_engine.generate_all_assessments(astro_data.birth_chart)
        
        # Return specific test result
        test_result = getattr(full_assessment, test_type.value)
        if not test_result:
            raise HTTPException(status_code=400, detail=f"Unable to generate {test_type.value} assessment")
        
        return {
            "test_type": test_type.value,
            "result": test_result,
            "birth_data": birth_data.dict(),
            "confidence_score": full_assessment.confidence_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating {test_type.value} assessment: {str(e)}")

@router.get("/tests")
async def get_available_tests():
    """
    Get list of available personality tests
    """
    return {
        "tests": [
            {"id": "mbti", "name": "Myers-Briggs Type Indicator", "description": "16 personality types"},
            {"id": "big_five", "name": "Big Five (OCEAN)", "description": "Five major personality dimensions"},
            {"id": "enneagram", "name": "Enneagram", "description": "9 personality types with wings"},
            {"id": "disc", "name": "DISC Assessment", "description": "Behavioral assessment tool"},
            {"id": "strengths_finder", "name": "StrengthsFinder", "description": "Top 5 strengths from 34 themes"},
            {"id": "love_languages", "name": "Love Languages", "description": "5 ways people express and receive love"},
            {"id": "attachment_styles", "name": "Attachment Styles", "description": "How you form emotional bonds"},
            {"id": "emotional_intelligence", "name": "Emotional Intelligence", "description": "EQ assessment"},
            {"id": "career_personality", "name": "Career Personality", "description": "Holland Code career matching"}
        ]
    }

@router.get("/health")
async def personality_health():
    """Health check for personality service"""
    return {"status": "healthy", "service": "personality-engine"}