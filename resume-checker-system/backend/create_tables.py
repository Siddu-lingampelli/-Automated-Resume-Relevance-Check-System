from app.db.database import engine, Base
from app.models import models

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("✅ Database tables created successfully!")