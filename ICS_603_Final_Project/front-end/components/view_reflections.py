from fasthtml.common import *
import httpx
from datetime import datetime

API_BASE = "http://localhost:9000"

USERS = [
    {"id": 1, "first_name": "John", "email": "john@test.com"},
    {"id": 2, "first_name": "Jane", "email": "jane@test.com"}
]

async def view_reflections(selected_user_id: int = None):
    query = f"?user_id={selected_user_id}" if selected_user_id else ""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_BASE}/api/reflections{query}")
        reflections = response.json()
    
    user_select = Form(
        Div(
            Label("Select User:", style="font-weight: 600; color: #333; margin-bottom: 8px; display: block;"),
            Select(
                Option("All Users", value="all", selected=(selected_user_id is None)), 
                *[
                    Option(f"{u['first_name']}", value=str(u["id"]), selected=(u["id"] == selected_user_id))
                    for u in USERS
                ],
                name="user_id",
                onchange="this.form.submit()",
                style="padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; min-width: 200px; background: white;"
            ),
            style="margin-bottom: 25px;"
        ),
        Input(type="hidden", name="tab", value="view"),
        method="get",
        action="/reflections/"
    )
    
    user_dict = {u["id"]: u["first_name"] for u in USERS}
    reflection_rows = [
        Tr(
            Td(
                A(r["title"], href=f"/reflections/?tab=view&id={r['id']}", 
                  style="color: #1976d2; text-decoration: none; font-weight: 500; hover:text-decoration: underline;"),
                style="padding: 12px 10px;"
            ),
            Td(", ".join(r["topics"]), style="color: #555;"),
            Td(
                datetime.fromisoformat(r["timestamp"].replace('Z', '+00:00')).strftime('%Y-%m-%d %I:%M %p'),
                style="color: #666; font-size: 0.95em;"
            ),
            Td(user_dict.get(r["user_id"], "Unknown"), style="color: #555;"),
            style="border-bottom: 1px solid #f0f0f0;"
        )
        for r in reflections
    ]
    
    return Main(
        user_select, 
        Table(
            Thead(
                Tr(
                    Th("Title", style="text-align: left; padding: 12px; background: #f8f9fa; color: #333; font-weight: 600; border-bottom: 2px solid #dee2e6;"),
                    Th("Topics", style="text-align: left; padding: 12px; background: #f8f9fa; color: #333; font-weight: 600; border-bottom: 2px solid #dee2e6;"),
                    Th("Date", style="text-align: left; padding: 12px; background: #f8f9fa; color: #333; font-weight: 600; border-bottom: 2px solid #dee2e6;"),
                    Th("User", style="text-align: left; padding: 12px; background: #f8f9fa; color: #333; font-weight: 600; border-bottom: 2px solid #dee2e6;")
                )
            ),
            Tbody(*reflection_rows),
            style="width: 100%; border-collapse: collapse; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden;"
        ),
        style="padding: 20px; max-width: 1400px; margin: 0 auto;"
    )