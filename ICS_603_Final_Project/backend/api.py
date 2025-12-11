"""
REST API for Reflection Management
"""
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Topic, Reflection
from classifier import classify_reflection_topics
from embeddings import embed_text
from recommender import generate_recommendation
import chromadb

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="reflections")

# ============================================================================
# Load Environment Variables
# ============================================================================
load_dotenv()

SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")
# os.getenv("OPENAI_API_KEY")

# ============================================================================
# Database Setup
# ============================================================================
engine = create_engine(
    SUPABASE_DB_URL,      
    pool_recycle=280,        
    pool_size=5,             
    max_overflow=10          
)
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
    user_id: int

class ClassifyReflectionOutput(BaseModel):
    topics: List[str]

class CreateReflectionInput(BaseModel):
    title: str
    text: str
    timestamp: datetime
    topics: List[str]
    user_id: int

class CreateReflectionOutput(BaseModel):
    reflection_id: int

class TopicsInput(BaseModel):
    names: List[str]

class TopicOutput(BaseModel):
    id: int
    name: str

class SearchInput(BaseModel):
    query: str
    user_id: Optional[int] = None
    
class RecommendationInput(BaseModel):
    user_id: int
    context: str
    prompt: str

class RecommendationOutput(BaseModel):
    recommendation: str
    reflections_used: List[dict]

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
        embedding = await embed_text(reflection.text)
        db_reflection = Reflection(
            title=reflection.title,
            text=reflection.text,
            timestamp=reflection.timestamp,
            user_id=reflection.user_id,
        )
        
        db.add(db_reflection)
        
        for topic_name in reflection.topics:
            topic = db.query(Topic).filter(Topic.name == topic_name).first()
            if not topic:
                topic = Topic(name=topic_name)
                db.add(topic)
            db_reflection.topic_list.append(topic)
        
        db.commit()
        db.refresh(db_reflection)
        
        collection.add(
            ids=[str(db_reflection.id)],
            embeddings=[embedding],
            metadatas=[{
                "title": reflection.title,
                "user_id": reflection.user_id 
            }]
        )
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
            "topics": [t.name for t in db_reflection.topic_list],
            "user_id": db_reflection.user_id 
        }
    finally:
        db.close()

@app.get("/api/reflections")
async def get_all_reflections(user_id: Optional[int] = None):
    """Retrieve all reflections"""
    db = SessionLocal()
    try:
        query = db.query(Reflection)
        if user_id:
            query = query.filter(Reflection.user_id == user_id)
        reflections = query.all()
        return [
            {
                "id": r.id,
                "title": r.title,
                "text": r.text,
                "timestamp": r.timestamp,
                "topics": [t.name for t in r.topic_list],
                "user_id": r.user_id 
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
        
        result = await classify_reflection_topics(
            reflection.title,
            reflection.text,
            existing_topic_names
        )
        
        return ClassifyReflectionOutput(topics=result.topics)
    finally:
        db.close()

@app.post("/api/reflections/search")
async def search_reflections(data: SearchInput):
    """Search reflections based on a query"""
    print("Collection count:", collection.count())
    query_embedding = await embed_text(data.query)

    query_params = {
        "query_embeddings": [query_embedding],
        "n_results": 10
    }
    
    if data.user_id is not None:
        query_params["where"] = {"user_id": data.user_id}
    
    results = collection.query(**query_params)
    
    print("Results:", results)
    print("Distances:", results["distances"][0])
    
    ids = []
    for id, distance in zip(results["ids"][0], results["distances"][0]):
        if distance < 1.35:
            ids.append(int(id))
    
    if not ids:
        return []

    db = SessionLocal()
    try:
        reflections = db.query(Reflection).filter(Reflection.id.in_(ids)).all()
        reflection_dict = {r.id: r for r in reflections}
        ordered_reflections = [reflection_dict[id] for id in ids if id in reflection_dict]
        
        return [
            {
                "id": r.id,
                "title": r.title,
                "text": r.text,
                "timestamp": r.timestamp,
                "topics": [t.name for t in r.topic_list],
                "user_id": r.user_id
            }
            for r in ordered_reflections
        ]
    finally:
        db.close()


@app.post("/api/recommendations", response_model=RecommendationOutput)
async def get_recommendation(data: RecommendationInput):
    """Generate a recommendation based on user's reflections"""
    # Get embedding and search for relevant reflections
    query_embedding = await embed_text(data.context)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10,
        where={"user_id": data.user_id} 
    )
    print("Recommendation search results:", results) 
    print("Distances:", results["distances"][0])
    
    # Filter by distance threshold and get IDs
    ids = [
        int(id) for id, distance in zip(results["ids"][0], results["distances"][0])
        if distance < 1.35
    ]
    
    if not ids:
        return RecommendationOutput(
            recommendation="I don't have enough information from your reflections to make a personalized recommendation. Try adding more reflections first.",
            reflections_used=[]
        )
    
    # Get reflections from database
    db = SessionLocal()
    try:
        reflections = db.query(Reflection).filter(Reflection.id.in_(ids)).all()
        
        # Format reflections and generate recommendation
        reflection_dicts = [
            {
                "id": r.id,
                "title": r.title,
                "text": r.text,
                "topics": [t.name for t in r.topic_list]
            }
            for r in reflections
        ]
        
        recommendation = await generate_recommendation(
            data.prompt,
            data.context,
            reflection_dicts
        )
        
        return RecommendationOutput(
            recommendation=recommendation,
            reflections_used=reflection_dicts
        )
    finally:
        db.close()

# ============================================================================
# Run the application
# ============================================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="localhost", port=9000, reload=True)

    
