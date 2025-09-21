from sqlalchemy import create_engine, text
from app.config import settings

def init_database():
    # Create a temporary engine without specific database
    temp_url = settings.DATABASE_URL.rsplit('/', 1)[0] + '/postgres'
    temp_engine = create_engine(temp_url)
    
    conn = temp_engine.connect()
    conn.execute(text("commit"))  # Close any open transactions
    
    try:
        # Create user if not exists
        conn.execute(text("CREATE USER resume_user WITH PASSWORD 'resume_pass';"))
    except Exception as e:
        print(f"User creation error (might already exist): {e}")
    
    try:
        # Create database if not exists
        conn.execute(text("CREATE DATABASE resume_checker OWNER resume_user;"))
    except Exception as e:
        print(f"Database creation error (might already exist): {e}")
    
    conn.close()
    temp_engine.dispose()

if __name__ == "__main__":
    init_database()
    print("✅ Database initialized successfully!")