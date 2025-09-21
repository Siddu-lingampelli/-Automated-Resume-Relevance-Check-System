import fitz, docx2txt, re, tempfile
from sentence_transformers import SentenceTransformer, util
from .gemini_service import GeminiService

model = SentenceTransformer("all-MiniLM-L6-v2")
gemini_service = GeminiService()

def extract_text(path: str):
    if path.endswith(".pdf"):
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    else:
        return docx2txt.process(path)

def clean_text(text: str):
    return re.sub(r"\\s+", " ", text).lower()

async def score_resume(jd_text: str, resume_text: str):
    # Traditional scoring
    jd_words = set(re.findall(r'\\b\\w+\\b', jd_text))
    res_words = set(re.findall(r'\\b\\w+\\b', resume_text))
    hard_score = len(jd_words & res_words) / max(len(jd_words),1) * 100
    embeddings = model.encode([jd_text, resume_text])
    soft_score = util.cos_sim(embeddings[0], embeddings[1]).item() * 100
    technical_score = 0.7*hard_score + 0.3*soft_score
    
    # Gemini AI analysis
    gemini_analysis = gemini_service.evaluate_resume(resume_text, jd_text)
    
    # Combine both analyses
    final_score = (technical_score + gemini_analysis["match_score"]) / 2
    verdict = "High" if final_score >= 75 else "Medium" if final_score >= 50 else "Low"
    
    return {
        "score": round(final_score, 2),
        "verdict": verdict,
        "technical_score": round(technical_score, 2),
        "gemini_score": gemini_analysis["match_score"],
        "key_strengths": gemini_analysis["key_strengths"],
        "areas_for_improvement": gemini_analysis["areas_for_improvement"],
        "missing_skills": gemini_analysis["missing_skills"],
        "suggestions": gemini_analysis["suggestions"],
        "detailed_feedback": gemini_analysis["detailed_feedback"]
    }

async def evaluate_resume_file(file, jd: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
        tmp.write(await file.read())
        text = extract_text(tmp.name)
    return await score_resume(jd, clean_text(text))
