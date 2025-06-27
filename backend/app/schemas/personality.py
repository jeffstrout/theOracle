from pydantic import BaseModel
from typing import List, Dict, Optional
from enum import Enum

class PersonalityTestType(str, Enum):
    MBTI = "mbti"
    BIG_FIVE = "big_five"
    ENNEAGRAM = "enneagram"
    DISC = "disc"
    STRENGTHS_FINDER = "strengths_finder"
    LOVE_LANGUAGES = "love_languages"
    ATTACHMENT_STYLES = "attachment_styles"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    CAREER_PERSONALITY = "career_personality"

class MBTIResult(BaseModel):
    type: str  # e.g., "ENFP"
    description: str
    strengths: List[str]
    weaknesses: List[str]
    careers: List[str]

class BigFiveResult(BaseModel):
    openness: int  # 1-100
    conscientiousness: int
    extraversion: int
    agreeableness: int
    neuroticism: int
    description: str

class EnneagramResult(BaseModel):
    type: int  # 1-9
    wing: Optional[int]
    description: str
    core_motivation: str
    basic_fear: str
    strengths: List[str]

class DISCResult(BaseModel):
    dominance: int  # 1-100
    influence: int
    steadiness: int
    conscientiousness: int
    primary_style: str
    description: str

class StrengthsFinderResult(BaseModel):
    top_strengths: List[str]  # Top 5 from 34 themes
    descriptions: Dict[str, str]

class LoveLanguagesResult(BaseModel):
    primary: str
    secondary: str
    scores: Dict[str, int]  # All 5 languages with scores

class AttachmentStyleResult(BaseModel):
    style: str  # Secure, Anxious, Avoidant, Disorganized
    percentage: int
    description: str
    characteristics: List[str]

class EmotionalIntelligenceResult(BaseModel):
    overall_eq: int  # 1-100
    self_awareness: int
    self_regulation: int
    motivation: int
    empathy: int
    social_skills: int
    description: str

class CareerPersonalityResult(BaseModel):
    holland_code: str  # e.g., "RIA"
    primary_type: str
    career_matches: List[str]
    work_environments: List[str]

class PersonalityAssessment(BaseModel):
    user_id: str
    birth_data: Dict
    mbti: Optional[MBTIResult] = None
    big_five: Optional[BigFiveResult] = None
    enneagram: Optional[EnneagramResult] = None
    disc: Optional[DISCResult] = None
    strengths_finder: Optional[StrengthsFinderResult] = None
    love_languages: Optional[LoveLanguagesResult] = None
    attachment_styles: Optional[AttachmentStyleResult] = None
    emotional_intelligence: Optional[EmotionalIntelligenceResult] = None
    career_personality: Optional[CareerPersonalityResult] = None
    created_at: str
    confidence_score: float  # 0-1