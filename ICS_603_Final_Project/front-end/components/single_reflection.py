from fasthtml.common import *
import httpx
from datetime import datetime

API_BASE = "http://localhost:9000"

USERS = [
    {"id": 1, "first_name": "John", "email": "john@test.com"},
    {"id": 2, "first_name": "Jane", "email": "jane@test.com"}
]

async def single_reflection(reflection_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/api/reflections/{reflection_id}")
        r = response.json()

    dt = datetime.fromisoformat(r["timestamp"].replace('Z', '+00:00'))
    formatted_date = dt.strftime("%Y-%m-%d %I:%M %p")

    user_dict = {u["id"]: u["first_name"] for u in USERS}
    user_name = user_dict.get(r["user_id"], "Unknown")
    
    return Card(
        Div(
            H2(r["title"], style="margin-top: 0; color: #333;"),
            Hr(style="border: none; border-top: 2px solid #e0e0e0; margin: 15px 0;"),
            P(r["text"], style="line-height: 1.6; color: #555; white-space: pre-wrap;"),
            Div(
                Span("Topics: ", style="margin-right: 5px;"),
                *[
                    Span(
                        topic, 
                        style="background: #e3f2fd; padding: 4px 10px; border-radius: 12px; margin-right: 8px; font-size: 0.9em; color: #1976d2;"
                    ) for topic in r["topics"]
                ],
                style="margin-top: 20px;"
            ),
            P(
                f"Date: {formatted_date}", 
            ),
            P(
                f"User: {user_name}",
            ),
            style="padding: 25px;"
        ),
        style="max-width: 800px; margin: 20px auto; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; background: white;"
    )