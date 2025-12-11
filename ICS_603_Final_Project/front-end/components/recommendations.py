from fasthtml.common import *
from markdown import markdown
from utils.constants import USERS

async def recommendations_form(user_id: int = None, context: str = "", prompt: str = "", recommendation: str = None, reflections_used: list = None):
    user_select = Select(
        name="user_id",
        *[Option(u["first_name"], value=str(u["id"]), selected=(u["id"] == user_id)) for u in USERS],
        required=True,
        style="""
            width: 100%;
            padding: 10px 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            font-family: 'Inter', sans-serif;
            color: #1e293b;
            transition: all 0.3s ease;
            cursor: pointer;
        """,
        onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'",
        onblur="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none'"
    )
    
    form = Div(
        # Header
        Div(
            Span("💡", style="font-size: 32px; margin-right: 12px;"),
            H2(
                "Get AI Recommendations",
                style="""
                    font-size: 24px;
                    font-weight: 700;
                    color: #1e293b;
                    margin: 0;
                    display: inline-block;
                """
            ),
            style="display: flex; align-items: center; margin-bottom: 8px;"
        ),
        P(
            "Get personalized recommendations based on your reflections and preferences.",
            style="""
                color: #64748b;
                font-size: 14px;
                margin: 0 0 32px 0;
            """
        ),
        
        # Form
        Form(
            Div(
                Label(
                    "User",
                    style="""
                        font-weight: 600;
                        color: #1e293b;
                        margin-bottom: 8px;
                        display: block;
                        font-size: 14px;
                    """
                ),
                user_select,
                style="margin-bottom: 24px;"
            ),
            Div(
                Label(
                    "Context",
                    style="""
                        font-weight: 600;
                        color: #1e293b;
                        margin-bottom: 8px;
                        display: block;
                        font-size: 14px;
                    """
                ),
                P(
                    "What topic or area do you want recommendations about?",
                    style="""
                        font-size: 13px;
                        color: #64748b;
                        margin-bottom: 8px;
                    """
                ),
                Textarea(
                    name="context",
                    rows="3",
                    required=True,
                    placeholder='e.g., "What I enjoy eating" or "My fitness interests"',
                    value=context,
                    style="""
                        width: 100%;
                        padding: 12px;
                        border: 2px solid #e2e8f0;
                        border-radius: 8px;
                        font-size: 14px;
                        font-family: 'Inter', sans-serif;
                        resize: vertical;
                        box-sizing: border-box;
                        line-height: 1.6;
                        transition: all 0.3s ease;
                        color: #1e293b;
                    """,
                    onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'",
                    onblur="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none'"
                ),
                style="margin-bottom: 24px;"
            ),
            Div(
                Label(
                    "Prompt",
                    style="""
                        font-weight: 600;
                        color: #1e293b;
                        margin-bottom: 8px;
                        display: block;
                        font-size: 14px;
                    """
                ),
                P(
                    "What specific recommendation do you need?",
                    style="""
                        font-size: 13px;
                        color: #64748b;
                        margin-bottom: 8px;
                    """
                ),
                Textarea(
                    name="prompt",
                    rows="3",
                    required=True,
                    placeholder='e.g., "Recommend me some options on where I should eat dinner today"',
                    value=prompt,
                    style="""
                        width: 100%;
                        padding: 12px;
                        border: 2px solid #e2e8f0;
                        border-radius: 8px;
                        font-size: 14px;
                        font-family: 'Inter', sans-serif;
                        resize: vertical;
                        box-sizing: border-box;
                        line-height: 1.6;
                        transition: all 0.3s ease;
                        color: #1e293b;
                    """,
                    onfocus="this.style.borderColor='#667eea'; this.style.boxShadow='0 0 0 3px rgba(102, 126, 234, 0.1)'",
                    onblur="this.style.borderColor='#e2e8f0'; this.style.boxShadow='none'"
                ),
                style="margin-bottom: 32px;"
            ),
            Button(
                "✨ Get Recommendation",
                type="submit",
                style="""
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 12px 32px;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
                    font-family: 'Inter', sans-serif;
                """,
                onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 4px 8px rgba(102, 126, 234, 0.4)'",
                onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(102, 126, 234, 0.3)'"
            ),
            action="/reflections/recommend",
            method="post"
        ),
        style="""
            max-width: 800px;
            margin: 0 auto 32px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border-radius: 12px;
            background: white;
            border: 1px solid #e2e8f0;
        """
    )
    
    if recommendation:
        result_card = Div(
            # Result header
            Div(
                Span(style="font-size: 32px; margin-right: 12px;"),
                H3(
                    "Your Recommendation",
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
            
            # Recommendation content
            Div(
                Div(
                    NotStr(markdown(recommendation)),
                    style="""
                        line-height: 1.8;
                        color: #334155;
                        font-size: 15px;
                        font-family: 'Inter', sans-serif;
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
            Hr(style="border: none; border-top: 2px solid #e2e8f0; margin: 32px 0;"),
            
            # Reflections used section
            Div(
                H4(
                    "📚 Based on these reflections",
                    style="""
                        color: #475569;
                        font-size: 16px;
                        font-weight: 700;
                        margin: 0 0 16px 0;
                    """
                ),
                Div(
                    *[
                        Div(
                            A(
                                Div(
                                    Strong(
                                        r["title"],
                                        style="""
                                            color: #667eea;
                                            font-size: 15px;
                                            display: block;
                                            margin-bottom: 6px;
                                        """
                                    ),
                                    Div(
                                        *[
                                            Span(
                                                topic,
                                                style="""
                                                    display: inline-block;
                                                    padding: 3px 8px;
                                                    background: #f1f5f9;
                                                    color: #475569;
                                                    border-radius: 6px;
                                                    font-size: 11px;
                                                    margin-right: 4px;
                                                    font-weight: 500;
                                                """
                                            ) for topic in r["topics"]
                                        ],
                                        style="display: flex; flex-wrap: wrap; gap: 4px;"
                                    ),
                                    style="padding: 0;"
                                ),
                                href=f"/reflections/?tab=view&id={r['id']}",
                                style="""
                                    text-decoration: none;
                                    display: block;
                                    transition: all 0.2s ease;
                                """
                            ),
                            style="""
                                padding: 16px;
                                background: white;
                                border-radius: 8px;
                                border: 1px solid #e2e8f0;
                                margin-bottom: 12px;
                                transition: all 0.3s ease;
                            """,
                            onmouseover="this.style.borderColor='#667eea'; this.style.transform='translateX(4px)'",
                            onmouseout="this.style.borderColor='#e2e8f0'; this.style.transform='translateX(0)'"
                        )
                        for r in (reflections_used or [])
                    ] if reflections_used else [
                        P(
                            "No reflections were used for this recommendation.",
                            style="""
                                color: #94a3b8;
                                font-style: italic;
                                text-align: center;
                                padding: 20px;
                            """
                        )
                    ]
                )
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
        )
        return Div(form, result_card, style="padding: 0;")
    
    return Div(form, style="padding: 0;")