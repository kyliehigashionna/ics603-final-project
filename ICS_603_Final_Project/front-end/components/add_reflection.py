from fasthtml.common import *
from services.reflection_service import classify_and_create_reflection
from utils.constants import USERS

def add_reflection_form():
    user_select = Select(
        name="user_id",
        *[Option(u["first_name"], value=str(u["id"])) for u in USERS],
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
        
    return Main(
        Div(
            # Header section
            Div(
                Div(
                    Span("✨", style="font-size: 32px; margin-right: 12px;"),
                    H2(
                        "Add New Reflection",
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
                    "Capture your thoughts, insights, and moments of growth.",
                    style="""
                        color: #64748b;
                        font-size: 14px;
                        margin: 0;
                    """
                ),
                style="margin-bottom: 32px;"
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
                        "Title",
                        style="""
                            font-weight: 600;
                            color: #1e293b;
                            margin-bottom: 8px;
                            display: block;
                            font-size: 14px;
                        """
                    ),
                    Input(
                        name="title", 
                        required=True,
                        placeholder="What's on your mind?",
                        style="""
                            width: 100%;
                            padding: 10px 12px;
                            border: 2px solid #e2e8f0;
                            border-radius: 8px;
                            font-size: 14px;
                            box-sizing: border-box;
                            font-family: 'Inter', sans-serif;
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
                        "Reflection",
                        style="""
                            font-weight: 600;
                            color: #1e293b;
                            margin-bottom: 8px;
                            display: block;
                            font-size: 14px;
                        """
                    ),
                    Textarea(
                        name="text", 
                        rows="10", 
                        required=True,
                        placeholder="Write your thoughts here... What did you learn? How do you feel? What are you grateful for?",
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
                Div(
                    Button(
                        "✨ Save Reflection", 
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
                    Button(
                        "Cancel",
                        type="button",
                        onclick="window.location.href='/reflections/?tab=view'",
                        style="""
                            background: white;
                            color: #64748b;
                            padding: 12px 32px;
                            border: 2px solid #e2e8f0;
                            border-radius: 8px;
                            font-size: 14px;
                            font-weight: 600;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            font-family: 'Inter', sans-serif;
                            margin-left: 12px;
                        """,
                        onmouseover="this.style.borderColor='#cbd5e1'; this.style.color='#475569'",
                        onmouseout="this.style.borderColor='#e2e8f0'; this.style.color='#64748b'"
                    ),
                    style="display: flex; align-items: center;"
                ),
                action="/reflections/create",
                method="post"
            ),
            style="""
                max-width: 700px;
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
    
async def create_reflection(title: str, text: str, user_id: int):
    user_id = int(user_id)
    await classify_and_create_reflection(title, text, user_id)
    return RedirectResponse("/reflections/?tab=view", status_code=303)