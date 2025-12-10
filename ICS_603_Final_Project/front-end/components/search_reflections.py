from fasthtml.common import *
import httpx
from datetime import datetime

API_BASE = "http://localhost:9000"

USERS = [
    {"id": 1, "first_name": "John", "email": "john@test.com"},
    {"id": 2, "first_name": "Jane", "email": "jane@test.com"}
]

async def search_reflections(search_query: str = "", selected_user_id: int = None):
    reflections = []
    if search_query:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_BASE}/api/reflections/search",
                json={"query": search_query}
            )
            reflections = response.json()
        
        if selected_user_id:
            reflections = [r for r in reflections if r["user_id"] == selected_user_id]
    
    user_dict = {u["id"]: u["first_name"] for u in USERS}
    
    search_user_form = Form(
        Div(
            Input(
                name="query",
                value=search_query,
                placeholder="Search reflections...",
                style=(
                    "flex: 1; padding: 10px 14px; "
                    "border: 1px solid #ddd; border-radius: 25px 0 0 25px; "
                    "outline: none; font-size: 15px;"
                )
            ),
            Select(
                Option("All Users", value="all", selected=(selected_user_id is None)),
                *[
                    Option(u["first_name"], value=str(u["id"]), selected=(u["id"] == selected_user_id))
                    for u in USERS
                ],
                name="user_id",
                style="padding: 8px 12px; border: 1px solid #ddd; border-radius: 0; font-size: 1em; background: white;"
            ),
            Button(
                "Search",
                type="submit",
                style=(
                    "padding: 10px 18px; border-radius: 0 25px 25px 0; "
                    "background-color: #4A90E2; color: white; "
                    "border: none; cursor: pointer; font-size: 15px;"
                )
            ),
            style="display: flex; justify-content: center; max-width: 600px; margin: 0 auto 24px;"
        ),
        Input(type="hidden", name="tab", value="search"), 
        method="get",
        action="/reflections/"
    )

    cards = [
        Card(
            Div(
                H3(r["title"], style="margin-top: 0; color: #333;"),
                Hr(style="border: none; border-top: 2px solid #e0e0e0; margin: 10px 0;"),
                P(r["text"], style="line-height: 1.6; color: #555; white-space: pre-wrap;"),
                Div(
                    Span("Topics: ", style="margin-right: 5px;"),
                    *[
                        Span(
                            topic, 
                            style="background: #e3f2fd; padding: 4px 10px; border-radius: 12px; margin-right: 8px; font-size: 0.9em; color: #1976d2;"
                        ) for topic in r["topics"]
                    ],
                    style="margin-top: 15px;"
                ),
                P(
                    f"Date: {datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')).strftime('%Y-%m-%d %I:%M %p')}", 
                    style="color: #999; font-size: 0.9em; margin-top: 15px; font-style: italic;"
                ),
                P(
                    f"User: {user_dict.get(r['user_id'], 'Unknown')}",
                    style="color: #999; font-size: 0.9em; margin-top: 5px; font-style: italic;"
                ),
                style="padding: 20px;"
            ),
            style="box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; background: white; margin: 15px 0;"
        ) for r in reflections
    ]
    
    return Div(
        search_user_form,
        P(
            "No similar reflections found.",
            style="text-align: center; margin-top: 40px; font-size: 16px; font-style: italic;"
        ) if search_query and not cards else None,
        *cards
    )