from pydantic import BaseModel
from typing import List, Optional

class ResumeEval(BaseModel):
    jd: str
    score: float
    verdict: str
    technical_score: float
    gemini_score: float
    key_strengths: List[str]
    areas_for_improvement: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    detailed_feedback: str
