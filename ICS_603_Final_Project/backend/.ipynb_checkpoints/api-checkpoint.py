"""
REST API for Reflection Management
"""
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Topic, Reflection
from classifier import classify_reflection_topics

# ============================================================================
# Load Environment Variables
# ============================================================================
load_dotenv()

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
# os.getenv("OPENAI_API_KEY")

# ============================================================================
# Database Setup
# ============================================================================
engine = create_engine(SUPABASE_DB_URL)
SessionLocal = sessionmaker(bind=engine)

# ============================================================================
# FastAPI App
# ============================================================================
app = FastAPI(title="Reflection API")

# ============================================================================
# Pydantic Models
# ============================================================================
class ClassifyReflectionInput(BaseModel):
    title: str
    text: str
    timestamp: datetime

class ClassifyReflectionOutput(BaseModel):
    topics: List[str]

class CreateReflectionInput(BaseModel):
    title: str
    text: str
    timestamp: datetime
    topics: List[str]

class CreateReflectionOutput(BaseModel):
    reflection_id: int

class TopicsInput(BaseModel):
    names: List[str]

class TopicOutput(BaseModel):
    id: int
    name: str

# ============================================================================
# API Endpoints
# ============================================================================
@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/api/topics", response_model=List[TopicOutput])
async def create_topics(topics: TopicsInput):
    """Add one or more topics"""
    db = SessionLocal()
    try:
        created_topics = []
        for name in topics.names:
            existing = db.query(Topic).filter(Topic.name == name).first()
            if not existing:
                db_topic = Topic(name=name)
                db.add(db_topic)
                db.flush()
                created_topics.append(TopicOutput(id=db_topic.id, name=db_topic.name))
            else:
                created_topics.append(TopicOutput(id=existing.id, name=existing.name))
        db.commit()
        return created_topics
    finally:
        db.close()

@app.get("/api/topics", response_model=List[TopicOutput])
async def get_topics():
    """Get all topics"""
    db = SessionLocal()
    try:
        topics = db.query(Topic).all()
        return [TopicOutput(id=t.id, name=t.name) for t in topics]
    finally:
        db.close()

@app.post("/api/reflections", response_model=CreateReflectionOutput)
async def create_reflection(reflection: CreateReflectionInput):
    """Insert a reflection into the database"""
    db = SessionLocal()
    try:
        db_reflection = Reflection(
            title=reflection.title,
            text=reflection.text,
            timestamp=reflection.timestamp
        )
        
        for topic_name in reflection.topics:
            topic = db.query(Topic).filter(Topic.name == topic_name).first()
            if not topic:
                topic = Topic(name=topic_name)
                db.add(topic)
            db_reflection.topic_list.append(topic)
        
        db.add(db_reflection)
        db.commit()
        db.refresh(db_reflection)
        return CreateReflectionOutput(reflection_id=db_reflection.id)
    finally:
        db.close()

@app.get("/api/reflections/{reflection_id}")
async def get_reflection(reflection_id: int):
    """Retrieve a reflection by ID"""
    db = SessionLocal()
    try:
        db_reflection = db.query(Reflection).filter(Reflection.id == reflection_id).first()
        if not db_reflection:
            return {"error": "Reflection not found"}
        return {
            "title": db_reflection.title,
            "text": db_reflection.text,
            "timestamp": db_reflection.timestamp,
            "topics": [t.name for t in db_reflection.topic_list]
        }
    finally:
        db.close()

@app.get("/api/reflections")
async def get_all_reflections():
    """Retrieve all reflections"""
    db = SessionLocal()
    try:
        reflections = db.query(Reflection).all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "text": r.text,
                "timestamp": r.timestamp,
                "topics": [t.name for t in r.topic_list]
            }
            for r in reflections
        ]
    finally:
        db.close()        

@app.post("/api/reflections/classify", response_model=ClassifyReflectionOutput)
async def classify_reflection(reflection: ClassifyReflectionInput):
    """Classify topics from a reflection"""
    db = SessionLocal()
    try:
        all_topics = db.query(Topic).all()
        existing_topic_names = [t.name for t in all_topics]
        
        topics = await classify_reflection_topics(
            reflection.title,
            reflection.text,
            existing_topic_names
        )
        
        return ClassifyReflectionOutput(topics=topics)
    finally:
        db.close()

# ============================================================================
# Run the application
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="localhost", port=8000, reload=True)

    
