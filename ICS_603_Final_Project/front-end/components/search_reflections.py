from fasthtml.common import *
from datetime import datetime
from services.reflection_service import search_reflections
from utils.constants import USERS

async def search_reflections_component(search_query: str = "", selected_user_id: int = None):
    reflections = []
    if search_query:
        reflections = await search_reflections(search_query, user_id=selected_user_id)
    
    user_dict = {u["id"]: u["first_name"] for u in USERS}
    
    # Search form
    search_user_form = Form(
        Div(
            # Search input
            Input(
                name="query",
                value=search_query,
                placeholder="Search reflections by keywords, topics, or content...",
                style="""
                    flex: 1;
                    padding: 12px 20px;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px 0 0 12px;
                    outline: none;
                    font-size: 15px;
                    font-family: 'Inter', sans-serif;
                    color: #1e293b;
                    transition: all 0.3s ease;
                """,
                onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'",
                onblur="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none'"
            ),
            
            # User filter dropdown
            Select(
                Option("All Users", value="all", selected=(selected_user_id is None)),
                *[
                    Option(u["first_name"], value=str(u["id"]), selected=(u["id"] == selected_user_id))
                    for u in USERS
                ],
                name="user_id",
                style="""
                    padding: 12px 16px;
                    border: 2px solid #e2e8f0;
                    border-left: none;
                    border-right: none;
                    font-size: 14px;
                    background: white;
                    font-family: 'Inter', sans-serif;
                    color: #1e293b;
                    cursor: pointer;
                    min-width: 140px;
                """
            ),
            
            # Search button
            Button(
                "🔍 Search",
                type="submit",
                style="""
                    padding: 12px 28px;
                    border-radius: 0 12px 12px 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    cursor: pointer;
                    font-size: 15px;
                    font-weight: 600;
                    font-family: 'Inter', sans-serif;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
                """,
                onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(102, 126, 234, 0.4)'",
                onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(102, 126, 234, 0.3)'"
            ),
            
            style="""
                display: flex;
                max-width: 800px;
                margin: 0 auto 32px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                overflow: hidden;
            """
        ),
        Input(type="hidden", name="tab", value="search"), 
        method="get",
        action="/reflections/"
    )

    # Empty state when no search has been performed
    if not search_query:
        empty_state = Div(
            Div("🔍", style="font-size: 64px; margin-bottom: 16px; opacity: 0.5;"),
            H3("Search Your Reflections", style="color: #64748b; font-size: 20px; margin-bottom: 8px;"),
            P(
                "Enter keywords, topics, or phrases to find relevant reflections.",
                Br(),
                "Search will return at most 10 results.",
                style="color: #94a3b8; font-size: 14px;"
            ),
            style="""
                text-align: center;
                padding: 60px 20px;
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                max-width: 600px;
                margin: 0 auto;
            """
        )
        return Div(search_user_form, empty_state)
    
    # Empty state when search found no results
    if not reflections:
        no_results = Div(
            Div("📭", style="font-size: 64px; margin-bottom: 16px; opacity: 0.5;"),
            H3("No reflections found", style="color: #64748b; font-size: 20px; margin-bottom: 8px;"),
            P(f"No results for \"{search_query}\"", style="color: #94a3b8; font-size: 14px; margin-bottom: 16px;"),
            P("Try different keywords or check your spelling", style="color: #94a3b8; font-size: 13px;"),
            style="""
                text-align: center;
                padding: 60px 20px;
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                max-width: 600px;
                margin: 0 auto;
            """
        )
        return Div(search_user_form, no_results)

    # Results header
    results_header = Div(
        Span(style="font-size: 24px; margin-right: 12px;"),
        H2(
            f"Found {len(reflections)} result{'s' if len(reflections) != 1 else ''}",
            style="""
                font-size: 20px;
                font-weight: 700;
                color: #1e293b;
                margin: 0;
                display: inline-block;
            """
        ),
        style="""
            display: flex;
            align-items: center;
            margin-bottom: 24px;
        """
    )

    # Search result cards
    cards = [
        Div(
            # Title as clickable link
            A(
                H3(
                    r["title"],
                    style="""
                        margin: 0 0 16px 0;
                        font-size: 20px;
                        font-weight: 700;
                        color: #667eea;
                        transition: color 0.2s ease;
                    """
                ),
                href=f"/reflections/?tab=view&id={r['id']}",
                style="text-decoration: none;",
                onmouseover="this.querySelector('h3').style.color='#764ba2'",
                onmouseout="this.querySelector('h3').style.color='#667eea'"
            ),
            
            # Reflection text preview
            P(
                r["text"][:300] + ("..." if len(r["text"]) > 300 else ""),
                style="""
                    line-height: 1.8;
                    color: #475569;
                    white-space: pre-wrap;
                    margin-bottom: 20px;
                    font-size: 15px;
                """
            ),
            
            # Divider
            Hr(style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;"),
            
            # Topics
            Div(
                Span(
                    "Topics",
                    style="""
                        font-size: 12px;
                        font-weight: 700;
                        color: #64748b;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 8px;
                        display: block;
                    """
                ),
                Div(
                    *[
                        Span(
                            topic,
                            style="""
                                display: inline-block;
                                padding: 4px 10px;
                                background: #f1f5f9;
                                color: #475569;
                                border-radius: 6px;
                                font-size: 12px;
                                margin-right: 6px;
                                margin-bottom: 4px;
                                font-weight: 500;
                            """
                        ) for topic in r["topics"]
                    ],
                    style="display: flex; flex-wrap: wrap; gap: 4px;"
                ),
                style="margin-bottom: 16px;"
            ),
            
            # Meta information
            Div(
                # User badge
                Div(
                    Span("👤", style="margin-right: 6px;"),
                    Span(
                        user_dict.get(r["user_id"], "Unknown"),
                        style="font-weight: 600; color: #667eea;"
                    ),
                    style="""
                        display: inline-flex;
                        align-items: center;
                        padding: 4px 10px;
                        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
                        border-radius: 6px;
                        font-size: 13px;
                    """
                ),
                
                # Date
                Div(
                    Span("📅", style="margin-right: 6px;"),
                    Span(
                        datetime.fromisoformat(r["timestamp"].replace('Z', '+00:00')).strftime('%b %d, %Y'),
                        style="color: #64748b; font-weight: 500;"
                    ),
                    style="""
                        display: inline-flex;
                        align-items: center;
                        padding: 4px 10px;
                        background: #f8fafc;
                        border-radius: 6px;
                        font-size: 13px;
                    """
                ),
                
                style="display: flex; gap: 10px; flex-wrap: wrap;"
            ),
            
            style="""
                padding: 24px;
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                margin-bottom: 16px;
                transition: all 0.3s ease;
            """,
            onmouseover="this.style.boxShadow='0 4px 6px rgba(0, 0, 0, 0.1)'; this.style.transform='translateY(-2px)'",
            onmouseout="this.style.boxShadow='0 1px 3px rgba(0, 0, 0, 0.1)'; this.style.transform='translateY(0)'"
        ) for r in reflections
    ]
    
    return Div(
        search_user_form,
        results_header,
        *cards,
        style="max-width: 900px; margin: 0 auto;"
    )