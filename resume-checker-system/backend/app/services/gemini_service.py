import google.generativeai as genai
from typing import Dict, Any
from app.config import GEMINI_API_KEY

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

class GeminiService:
    def __init__(self):
        # Initialize the Gemini model (using the most capable model)
        self.model = genai.GenerativeModel('gemini-pro')

    def evaluate_resume(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """
        Evaluate a resume against a job description using Gemini AI.
        
        Args:
            resume_text (str): The text content of the resume
            job_description (str): The job description text
            
        Returns:
            Dict[str, Any]: Detailed evaluation including match score and suggestions
        """
        prompt = f"""
        You are an expert AI recruiter tasked with evaluating resumes against specific job requirements. Analyze the resume in detail, comparing it to the job description provided.

        Instructions for Analysis:
        1. First, extract key requirements from the job description (skills, experience, qualifications)
        2. Compare the resume against these requirements
        3. Provide a detailed evaluation focusing on:
           - Skills match
           - Experience relevance
           - Education/qualification alignment
           - Project/achievement relevance
        
        Job Description:
        {job_description}
        
        Resume:
        {resume_text}
        
        Provide your evaluation in the following JSON format:
        {{
            "match_score": <0-100 score based on overall match>,
            "key_strengths": [
                "specific strengths that align with the job requirements",
                "highlight matching skills and relevant experience"
            ],
            "areas_for_improvement": [
                "specific areas where the candidate needs development",
                "gaps between requirements and current profile"
            ],
            "missing_skills": [
                "required skills not found in resume",
                "technical or soft skills needed but not demonstrated"
            ],
            "suggestions": [
                "actionable suggestions to improve candidacy",
                "specific recommendations for skill development",
                "certification or training recommendations"
            ],
            "detailed_feedback": "A comprehensive paragraph evaluating the candidate's fit for this specific role, including:
                - How well they meet core requirements
                - Relevant experience analysis
                - Project/achievement relevance
                - Cultural fit indicators
                - Overall recommendation"
        }}

        Remember to:
        - Be specific and reference actual content from both the job description and resume
        - Focus on relevance to the specific role
        - Provide constructive, actionable feedback
        - Consider both technical and soft skills
        - Be objective and data-driven in scoring
        """

        # Input validation
        if not resume_text or not resume_text.strip():
            return {
                "match_score": 0,
                "key_strengths": [],
                "areas_for_improvement": ["Resume appears to be empty"],
                "missing_skills": [],
                "suggestions": ["Please provide a complete resume"],
                "detailed_feedback": "Unable to evaluate: Resume content is empty"
            }
        
        if not job_description or not job_description.strip():
            return {
                "match_score": 0,
                "key_strengths": [],
                "areas_for_improvement": [],
                "missing_skills": [],
                "suggestions": ["Please provide a job description"],
                "detailed_feedback": "Unable to evaluate: Job description is empty"
            }

        try:
            # Generate the evaluation using Gemini
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Empty response from Gemini API")

            # Parse the response text as a dictionary
            import json
            try:
                evaluation = json.loads(response.text)
            except json.JSONDecodeError:
                # If JSON parsing fails, try using eval as fallback
                evaluation = eval(response.text)
            
            # Validate the response structure
            required_fields = ["match_score", "key_strengths", "areas_for_improvement", 
                             "missing_skills", "suggestions", "detailed_feedback"]
            
            for field in required_fields:
                if field not in evaluation:
                    evaluation[field] = [] if field != "match_score" and field != "detailed_feedback" else ""
            
            # Ensure match_score is within valid range
            if not isinstance(evaluation["match_score"], (int, float)) or \
               evaluation["match_score"] < 0 or evaluation["match_score"] > 100:
                evaluation["match_score"] = 0
            
            # Ensure lists are actually lists
            for field in ["key_strengths", "areas_for_improvement", "missing_skills", "suggestions"]:
                if not isinstance(evaluation[field], list):
                    evaluation[field] = [str(evaluation[field])] if evaluation[field] else []
            
            return evaluation
            
        except Exception as e:
            # Log the error for debugging (you might want to use proper logging)
            print(f"Error in Gemini evaluation: {str(e)}")
            
            # Return a formatted error response
            return {
                "match_score": 0,
                "key_strengths": [],
                "areas_for_improvement": [],
                "missing_skills": [],
                "suggestions": ["Unable to complete evaluation"],
                "detailed_feedback": f"Error during evaluation: {str(e)}. Please try again or contact support if the issue persists."
            }