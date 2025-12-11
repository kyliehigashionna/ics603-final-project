from fasthtml.common import *
from components.add_reflection import add_reflection_form
from components.view_reflections import view_reflections
from components.single_reflection import single_reflection
from components.search_reflections import search_reflections_component
from components.recommendations import recommendations_form

async def reflections_page(tab: str = "add", id: int = None, user_id: str = None, query: str = "", recommendation_data: dict = None):
    selected_user_id = None
    if user_id and user_id != "all":
        selected_user_id = int(user_id)
    
    # Helper function for tab styling
    def tab_style(is_active):
        base = """
            padding: 8px 20px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        """
        if is_active:
            return base + """
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
            """
        else:
            return base + """
                background: white;
                color: #64748b;
                border: 1px solid #e2e8f0;
            """
    
    # Navigation header with gradient background
    header = Div(
        Div(
            # Compact header with centered tabs
            Div(
                A(
                    Span("←", style="font-size: 18px;"),
                    " Home",
                    href="/",
                    style="""
                        text-decoration: none;
                        color: #64748b;
                        font-size: 18px;
                        font-weight: 500;
                        transition: color 0.3s ease;
                    """,
                    onmouseover="this.style.color='#667eea'",
                    onmouseout="this.style.color='#64748b'"
                ),
                
                # Tab navigation - centered
                Div(
                    A("➕ Add", href="/reflections/?tab=add", 
                      style=tab_style(tab == "add" and not id),
                      onmouseover="if (!this.href.includes('tab=add') || this.style.background.includes('linear-gradient')) return; this.style.borderColor='#667eea'; this.style.color='#667eea'",
                      onmouseout="if (this.style.background.includes('linear-gradient')) return; this.style.borderColor='#e2e8f0'; this.style.color='#64748b'"
                    ),
                    A("📖 View", href="/reflections/?tab=view", 
                      style=tab_style(tab == "view" or id),
                      onmouseover="if (this.style.background.includes('linear-gradient')) return; this.style.borderColor='#667eea'; this.style.color='#667eea'",
                      onmouseout="if (this.style.background.includes('linear-gradient')) return; this.style.borderColor='#e2e8f0'; this.style.color='#64748b'"
                    ),
                    A("🔍 Search", href="/reflections/?tab=search",
                      style=tab_style(tab == "search"),
                      onmouseover="if (this.style.background.includes('linear-gradient')) return; this.style.borderColor='#667eea'; this.style.color='#667eea'",
                      onmouseout="if (this.style.background.includes('linear-gradient')) return; this.style.borderColor='#e2e8f0'; this.style.color='#64748b'"
                    ),
                    A("💡 Recommendations", href="/reflections/?tab=recommendations",
                      style=tab_style(tab == "recommendations"),
                      onmouseover="if (this.style.background.includes('linear-gradient')) return; this.style.borderColor='#667eea'; this.style.color='#667eea'",
                      onmouseout="if (this.style.background.includes('linear-gradient')) return; this.style.borderColor='#e2e8f0'; this.style.color='#64748b'"
                    ),
                    style="""
                        display: flex;
                        gap: 8px;
                        justify-content: center;
                        align-items: center;
                    """
                ),
                
                # Empty div for spacing balance
                Div(style="width: 60px;"),
                
                style="""
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    gap: 16px;
                """
            ),
            
            style="""
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px 20px;
            """
        ),
        style="""
            background: white;
            border-bottom: 1px solid #e2e8f0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        """
    )
    
    # Content area
    if tab == "add":
        content = add_reflection_form()
    elif tab == "recommendations":
        if recommendation_data:
            content = await recommendations_form(
                user_id=recommendation_data["user_id"],
                context=recommendation_data["context"],
                prompt=recommendation_data["prompt"],
                recommendation=recommendation_data["recommendation"],
                reflections_used=recommendation_data["reflections_used"]
            )
        else:
            content = await recommendations_form()
    elif id:
        content = await single_reflection(id)
    elif tab == "search":
        content = await search_reflections_component(search_query=query, selected_user_id=selected_user_id)
    else:
        content = await view_reflections(selected_user_id)
    
    # Wrap content in container
    content_wrapper = Div(
        content,
        style="""
            max-width: 1200px;
            margin: 0 auto;
            padding: 32px 20px;
        """
    )
    
    # Global styles
    styles = Style("""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f8fafc;
            color: #1e293b;
            min-height: 100vh;
        }
        
        /* Smooth scrolling */
        html {
            scroll-behavior: smooth;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            body {
                font-size: 14px;
            }
        }
    """)
    
    return Title("Reflections"), Main(
        styles,
        header,
        content_wrapper,
        style="margin: 0;"
    )