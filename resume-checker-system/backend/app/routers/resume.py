from fastapi import APIRouter, UploadFile, File, Form
from app.services.evaluator import evaluate_resume_file

router = APIRouter()

@router.post("/evaluate")
async def evaluate_resume(file: UploadFile = File(...), jd: str = Form(...)):
    """
    Evaluate a resume against a job description using both traditional methods and Gemini AI.
    
    Args:
        file: The resume file (PDF/DOC/DOCX)
        jd: The job description text
        
    Returns:
        Dict containing evaluation results including scores, strengths, and suggestions
    """
    return await evaluate_resume_file(file, jd)