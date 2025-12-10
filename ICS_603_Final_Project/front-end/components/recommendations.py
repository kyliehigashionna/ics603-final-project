from fasthtml.common import *

API_BASE = "http://localhost:9000"

USERS = [
    {"id": 1, "first_name": "John", "email": "john@test.com"},
    {"id": 2, "first_name": "Jane", "email": "jane@test.com"}
]

async def recommendations_form(user_id: int = None, context: str = "", prompt: str = "", recommendation: str = None, reflections_used: list = None):
    user_select = Select(
        name="user_id",
        *[Option(u["first_name"], value=str(u["id"]), selected=(u["id"] == user_id)) for u in USERS],
        required=True,
        style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; background: white; font-family: Arial, sans-serif;"
    )
    
    form = Card(
        H2("Get Recommendations", style="margin-top: 0; color: #333; margin-bottom: 20px;"),
        Form(
            Div(
                Label("User:", style="font-weight: 600; color: #333; margin-bottom: 6px; display: block;"),
                user_select,
                style="margin-bottom: 20px;"
            ),
            Div(
                Label("Context:", style="font-weight: 600; color: #333; margin-bottom: 6px; display: block;"),
                P("What topic or area do you want recommendations about?", style="font-size: 0.9em; color: #666; margin-bottom: 8px;"),
                Textarea(
                    name="context",
                    rows="3",
                    required=True,
                    placeholder='e.g., "What I enjoy eating" or "My fitness interests"',
                    value=context,
                    style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; font-family: Arial, sans-serif; resize: vertical; box-sizing: border-box;"
                ),
                style="margin-bottom: 20px;"
            ),
            Div(
                Label("Prompt:", style="font-weight: 600; color: #333; margin-bottom: 6px; display: block;"),
                P("What specific recommendation do you need?", style="font-size: 0.9em; color: #666; margin-bottom: 8px;"),
                Textarea(
                    name="prompt",
                    rows="3",
                    required=True,
                    placeholder='e.g., "Recommend me some options on where I should eat dinner today"',
                    value=prompt,
                    style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 1em; font-family: Arial, sans-serif; resize: vertical; box-sizing: border-box;"
                ),
                style="margin-bottom: 25px;"
            ),
            Button(
                "Get Recommendation",
                type="submit",
                style="background: #1976d2; color: white; padding: 12px 30px; border: none; border-radius: 6px; font-size: 1em; font-weight: 600; cursor: pointer; transition: background 0.2s;"
            ),
            action="/reflections/recommend",
            method="post"
        ),
        style="max-width: 800px; margin: 20px auto; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; background: white;"
    )
    
    if recommendation:
        result_card = Card(
            H3("Recommendation", style="margin-top: 0; color: #333; margin-bottom: 15px;"),
            Hr(style="border: none; border-top: 2px solid #e0e0e0; margin: 15px 0;"),
            P(recommendation, style="line-height: 1.8; color: #555; white-space: pre-wrap; font-size: 1.05em;"),
            Hr(style="border: none; border-top: 1px solid #f0f0f0; margin: 25px 0;"),
            H4("Based on these reflections:", style="color: #666; font-size: 1em; margin-bottom: 15px;"),
            Ul(
                *[
                    Li(
                        A(
                            Strong(r["title"], style="color: #1976d2;"),
                            href=f"/reflections/?tab=view&id={r['id']}",
                            style="text-decoration: none; color: #1976d2; hover: text-decoration: underline;"
                        ),
                        Span(f" - Topics: {', '.join(r['topics'])}", style="color: #666; font-size: 0.9em;"),
                        style="margin-bottom: 8px;"
                    )
                    for r in (reflections_used or [])
                ],
                style="list-style-type: disc; padding-left: 25px;"
            ) if reflections_used else P("No reflections were used.", style="color: #999; font-style: italic;"),
            style="max-width: 800px; margin: 20px auto; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; background: #f8f9fa;"
        )
        return Div(form, result_card, style="padding: 20px;")
    
    return Div(form, style="padding: 20px;")
