from fasthtml.common import *
from datetime import datetime
from services.reflection_service import get_all_reflections
from utils.constants import USERS

async def view_reflections(selected_user_id: int = None):
    reflections = await get_all_reflections(selected_user_id)
    
    user_select = Form(
        Div(
            Label(
                "Filter by User",
                style="""
                    font-weight: 600;
                    color: #1e293b;
                    margin-bottom: 8px;
                    display: block;
                    font-size: 14px;
                """
            ),
            Select(
                Option("All Users", value="all", selected=(selected_user_id is None)), 
                *[
                    Option(f"{u['first_name']}", value=str(u["id"]), selected=(u["id"] == selected_user_id))
                    for u in USERS
                ],
                name="user_id",
                onchange="this.form.submit()",
                style="""
                    padding: 10px 12px;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    font-size: 14px;
                    min-width: 200px;
                    background: white;
                    font-family: 'Inter', sans-serif;
                    color: #1e293b;
                    cursor: pointer;
                    transition: all 0.3s ease;
                """,
                onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'",
                onblur="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none'"
            ),
            style="""
                display: inline-block;
                padding: 20px 24px;
                background: white;
                border-radius: 6px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                margin-bottom: 10px;
            """
        ),
        Input(type="hidden", name="tab", value="view"),
        method="get",
        action="/reflections/"
    )
    
    user_dict = {u["id"]: u["first_name"] for u in USERS}
    
    # Empty state if no reflections
    if not reflections:
        empty_state = Div(
            Div("📝", style="font-size: 64px; margin-bottom: 16px; opacity: 0.5;"),
            H3("No reflections yet", style="color: #64748b; font-size: 20px; margin-bottom: 8px;"),
            P("Start capturing your thoughts and insights!", style="color: #94a3b8; font-size: 14px;"),
            A(
                "➕ Add Your First Reflection",
                href="/reflections/?tab=add",
                style="""
                    display: inline-block;
                    margin-top: 16px;
                    padding: 10px 24px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                """,
                onmouseover="this.style.transform='translateY(-2px)'",
                onmouseout="this.style.transform='translateY(0)'"
            ),
            style="""
                text-align: center;
                padding: 60px 20px;
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
            """
        )
        return Main(user_select, empty_state, style="padding: 0; max-width: 1400px; margin: 0 auto;")
    
    reflection_rows = [
        Tr(
            Td(
                A(
                    r["title"],
                    href=f"/reflections/?tab=view&id={r['id']}", 
                    style="""
                        color: #667eea;
                        text-decoration: none;
                        font-weight: 600;
                        transition: color 0.2s ease;
                        font-size: 14px;
                    """,
                    onmouseover="this.style.color='#764ba2'",
                    onmouseout="this.style.color='#667eea'"
                ),
                style="padding: 16px 16px;"
            ),
            Td(
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
                        )
                        for topic in r["topics"]
                    ],
                    style="display: flex; flex-wrap: wrap; gap: 4px;"
                ),
                style="padding: 16px 16px;"
            ),
            Td(
                datetime.fromisoformat(r["timestamp"].replace('Z', '+00:00')).strftime('%b %d, %Y • %I:%M %p'),
                style="""
                    color: #64748b;
                    font-size: 13px;
                    padding: 16px 16px;
                    white-space: nowrap;
                """
            ),
            Td(
                Span(
                    user_dict.get(r["user_id"], "Unknown"),
                    style="""
                        display: inline-block;
                        padding: 4px 12px;
                        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
                        color: #667eea;
                        border-radius: 6px;
                        font-size: 13px;
                        font-weight: 600;
                    """
                ),
                style="padding: 16px 16px;"
            ),
            style="""
                border-bottom: 1px solid #f1f5f9;
                transition: background-color 0.2s ease;
            """,
            onmouseover="this.style.backgroundColor='#f8fafc'",
            onmouseout="this.style.backgroundColor='transparent'"
        )
        for r in reflections
    ]
    
    return Main(
        Div(
            Div(
                Span(style="font-size: 24px; margin-right: 12px;"),
                H2(
                    f"All Reflections: {len(reflections)}",
                    style="""
                        font-size: 20px;
                        font-weight: 700;
                        color: #1e293b;
                        margin: 0;
                        display: inline-block;
                    """
                ),
                style="display: flex; align-items: center; margin-bottom: 24px;"
            ),
            user_select,
            style="margin-bottom: 24px;"
        ),
        Div(
            Table(
                Thead(
                    Tr(
                        Th(
                            "Title",
                            style="""
                                text-align: left;
                                padding: 14px 16px;
                                background: #f8fafc;
                                color: #475569;
                                font-weight: 700;
                                border-bottom: 2px solid #e2e8f0;
                                font-size: 13px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                            """
                        ),
                        Th(
                            "Topics",
                            style="""
                                text-align: left;
                                padding: 14px 16px;
                                background: #f8fafc;
                                color: #475569;
                                font-weight: 700;
                                border-bottom: 2px solid #e2e8f0;
                                font-size: 13px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                            """
                        ),
                        Th(
                            "Date & Time",
                            style="""
                                text-align: left;
                                padding: 14px 16px;
                                background: #f8fafc;
                                color: #475569;
                                font-weight: 700;
                                border-bottom: 2px solid #e2e8f0;
                                font-size: 13px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                            """
                        ),
                        Th(
                            "User",
                            style="""
                                text-align: left;
                                padding: 14px 16px;
                                background: #f8fafc;
                                color: #475569;
                                font-weight: 700;
                                border-bottom: 2px solid #e2e8f0;
                                font-size: 13px;
                                text-transform: uppercase;
                                letter-spacing: 0.5px;
                            """
                        )
                    )
                ),
                Tbody(*reflection_rows),
                style="""
                    width: 100%;
                    border-collapse: collapse;
                    background: white;
                    font-family: 'Inter', sans-serif;
                """
            ),
            style="""
                background: white;
                border-radius: 12px;
                border: 1px solid #e2e8f0;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            """
        ),
        style="padding: 0; max-width: 1400px; margin: 0 auto;"
    )