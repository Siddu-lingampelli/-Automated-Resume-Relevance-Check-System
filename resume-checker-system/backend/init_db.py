from app.db.database import Base, engine
from app.models import models   # ✅ this loads Job, User, Resume, Evaluation

if __name__ == "__main__":
    print("👉 Creating tables in PostgreSQL resume_checker DB...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")