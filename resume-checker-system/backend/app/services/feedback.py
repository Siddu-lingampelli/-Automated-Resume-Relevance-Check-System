def generate_feedback(missing_skills:list):
    return "Consider adding: " + ", ".join(missing_skills) if missing_skills else "Resume looks strong!"
