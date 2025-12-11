import httpx

API_BASE = "http://localhost:9000"

async def get_recommendation(user_id: int, context: str, prompt: str):
    """Fetch recommendation from the API backend."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{API_BASE}/api/recommendations",
            json={
                "user_id": user_id,
                "context": context,
                "prompt": prompt
            }
        )
        return response.json()