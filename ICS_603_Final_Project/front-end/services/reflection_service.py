import httpx
from datetime import datetime

API_BASE = "http://localhost:9000"

async def get_reflection(reflection_id: int):
    """Fetch a single reflection by ID."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/api/reflections/{reflection_id}")
        return response.json()

async def get_all_reflections(user_id: int = None):
    """Fetch all reflections, optionally filtered by user."""
    async with httpx.AsyncClient() as client:
        query = f"?user_id={user_id}" if user_id else ""
        response = await client.get(f"{API_BASE}/api/reflections{query}")
        return response.json()

async def search_reflections(query: str, user_id: int = None):
    """Search reflections by query."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE}/api/reflections/search",
            json={"query": query, "user_id": user_id}
        )
        return response.json()

async def classify_and_create_reflection(title: str, text: str, user_id: int):
    """Classify topics and create a new reflection."""
    async with httpx.AsyncClient() as client:
        # First classify
        classify_response = await client.post(
            f"{API_BASE}/api/reflections/classify",
            json={
                "title": title,
                "text": text,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id 
            }
        )
        topics = classify_response.json()["topics"]
        
        # Then create
        await client.post(
            f"{API_BASE}/api/reflections",
            json={
                "title": title,
                "text": text,
                "timestamp": datetime.now().isoformat(),
                "topics": topics,
                "user_id": user_id 
            }
        )