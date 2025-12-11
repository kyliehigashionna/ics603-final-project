from fasthtml.common import *
from datetime import datetime
from services.reflection_service import get_reflection
from utils.constants import USERS

async def single_reflection(reflection_id: int):
    r = await get_reflection(reflection_id)

    dt = datetime.fromisoformat(r["timestamp"].replace('Z', '+00:00'))
    formatted_date = dt.strftime("%b %d, %Y • %I:%M %p")

    user_dict = {u["id"]: u["first_name"] for u in USERS}
    user_name = user_dict.get(r["user_id"], "Unknown")
    
    return Div(
        # Back button
        Div(
            A(
                Span("←", style="font-size: 18px; margin-right: 8px;"),
                "Back to Reflections",
                href="/reflections/?tab=view",
                style="""
                    display: inline-flex;
                    align-items: center;
                    text-decoration: none;
                    color: #64748b;
                    font-size: 14px;
                    font-weight: 500;
                    transition: color 0.3s ease;
                    margin-bottom: 24px;
                """,
                onmouseover="this.style.color='#667eea'",
                onmouseout="this.style.color='#64748b'"
            ),
            style="max-width: 800px; margin: 0 auto;"
        ),
        
        # Main reflection card
        Div(
            # Title
            H1(
                r["title"],
                style="""
                    font-size: 32px;
                    font-weight: 700;
                    color: #1e293b;
                    margin: 0 0 32px 0;
                    line-height: 1.3;
                """
            ),
            
            # Reflection text content
            Div(
                Div(
                    r["text"],
                    style="""
                        line-height: 1.8;
                        color: #334155;
                        white-space: pre-wrap;
                        font-size: 16px;
                    """
                ),
                style="""
                    padding: 24px;
                    background: #f8fafc;
                    border-radius: 8px;
                    border-left: 4px solid #667eea;
                    margin-bottom: 32px;
                """
            ),
            
            # Divider
            Hr(
                style="""
                    border: none;
                    border-top: 2px solid #e2e8f0;
                    margin: 32px 0;
                """
            ),
            
            # Topics section
            Div(
                Div(
                    Span(
                        "Topics",
                        style="""
                            font-size: 13px;
                            font-weight: 700;
                            color: #475569;
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
                                    padding: 6px 14px;
                                    background: #f1f5f9;
                                    color: #475569;
                                    border-radius: 8px;
                                    font-size: 13px;
                                    margin-right: 8px;
                                    margin-bottom: 8px;
                                    font-weight: 600;
                                """
                            ) for topic in r["topics"]
                        ],
                        style="display: flex; flex-wrap: wrap; gap: 8px;"
                    ),
                    style="""
                        padding: 16px;
                        background: #f8fafc;
                        border-radius: 8px;
                        border: 1px solid #e2e8f0;
                    """
                ),
                style="margin-bottom: 24px;"
            ),
            
            # Meta information bar
            Div(
                # User badge
                Div(
                    Span("👤", style="margin-right: 6px;"),
                    Span(
                        user_name,
                        style="""
                            font-weight: 600;
                            color: #667eea;
                        """
                    ),
                    style="""
                        display: inline-flex;
                        align-items: center;
                        padding: 6px 14px;
                        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
                        border-radius: 8px;
                        font-size: 14px;
                    """
                ),
                
                # Date badge
                Div(
                    Span("📅", style="margin-right: 6px;"),
                    Span(
                        formatted_date,
                        style="""
                            color: #64748b;
                            font-weight: 500;
                        """
                    ),
                    style="""
                        display: inline-flex;
                        align-items: center;
                        padding: 6px 14px;
                        background: #f8fafc;
                        border-radius: 8px;
                        font-size: 14px;
                    """
                ),
                
                style="""
                    display: flex;
                    gap: 12px;
                    flex-wrap: wrap;
                """
            ),
            
            style="""
                max-width: 800px;
                margin: 0 auto;
                padding: 32px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                border-radius: 12px;
                background: white;
                border: 1px solid #e2e8f0;
            """
        ),
        
        style="padding: 0;"
    )