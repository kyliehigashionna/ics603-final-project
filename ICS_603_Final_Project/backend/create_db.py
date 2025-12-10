
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Topic, User

# ============================================================================
# Load Environment Variables
# ============================================================================
load_dotenv()
SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

if not SUPABASE_DB_URL:
    print("❌ ERROR: SUPABASE_DB_URL is not in .env file")
    exit(1)

# ============================================================================
# Database Setup
# ============================================================================
engine = create_engine(SUPABASE_DB_URL)
SessionLocal = sessionmaker(bind=engine)

# ============================================================================
# Create Tables
# ============================================================================
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    
    # Insert initial topics
    db = SessionLocal()
    try:
        users_to_add = [
            {"first_name": "John", "email": "john@test.com"},
            {"first_name": "Jane", "email": "jane@test.com"},
        ]
        user_objects = {}
        for user_data in users_to_add:
            user = db.query(User).filter(User.email == user_data["email"]).first()
            if not user:
                user = User(**user_data)
                db.add(user)
                db.flush()
            user_objects[user.first_name] = user

        initial_topics = ["learning", "surfing", "parenting", "arts", "productivity", "relationships", "health"]
        for topic_name in initial_topics:
            if not db.query(Topic).filter(Topic.name == topic_name).first():
                db.add(Topic(name=topic_name))
        db.commit()
        db.commit()
        print("✅ Tables created and topics seeded successfully!")
    finally:
        db.close()
