import os

class Settings:
    PROJECT_NAME: str = "Resume Checker"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./resume_checker.db"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret")  # later used for JWT
    DEBUG: bool = True
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "AIzaSyByENcLXfbZDD0gLhW8a6UpC3AJHF2vjp0")  # Add your Gemini API key here

settings = Settings()

# Export the Gemini API key for easy access
GEMINI_API_KEY = settings.GEMINI_API_KEY