from fasthtml.common import *
import httpx
from datetime import datetime

API_BASE = "http://localhost:9000"

USERS = [
    {"id": 1, "first_name": "John", "email": "john@test.com"},
    {"id": 2, "first_name": "Jane", "email": "jane@test.com"}
]

def add_reflection_form():
    user_select = Select(
        name="user_id",
        *[Option(u["first_name"], value=str(u["id"])) for u in USERS],
        style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; background: white; font-family: Arial, sans-serif;"
    )
        
    return Main(
        Card(
            H2("Add New Reflection", style="margin-top: 0; color: #333; margin-bottom: 20px;"),
            Form(            
                Div(
                    Label("User:", style="font-weight: 600; color: #333; margin-bottom: 6px; display: block;"),
                    user_select,
                    style="margin-bottom: 20px;"
                ),
                Div(
                    Label("Title:", style="font-weight: 600; color: #333; margin-bottom: 6px; display: block;"),
                    Input(
                        name="title", 
                        required=True,
                        placeholder="Enter reflection title...",
                        style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; box-sizing: border-box; font-family: Arial, sans-serif;"
                    ),
                    style="margin-bottom: 20px;"
                ),
                Div(
                    Label("Text:", style="font-weight: 600; color: #333; margin-bottom: 6px; display: block;"),
                    Textarea(
                        name="text", 
                        rows="10", 
                        required=True,
                        placeholder="Write your reflection here...",
                        style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; font-family: Arial, sans-serif; resize: vertical; box-sizing: border-box;"
                    ),
                    style="margin-bottom: 25px;"
                ),
                Button(
                    "Submit Reflection", 
                    type="submit",
                    style="background: #1976d2; color: white; padding: 12px 30px; border: none; border-radius: 6px; font-size: 1em; font-weight: 600; cursor: pointer; transition: background 0.2s;"
                ),
                action="/reflections/create",
                method="post"
            ),
            style="max-width: 700px; margin: 20px auto; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; background: white;"
        ),
        style="padding: 20px;"
    )   
    
async def create_reflection(title: str, text: str, user_id: int):
    user_id = int(user_id)
    async with httpx.AsyncClient() as client:
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
    
    return RedirectResponse("/reflections/?tab=view", status_code=303)