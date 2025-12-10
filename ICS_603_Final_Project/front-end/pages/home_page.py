from fasthtml.common import *

async def home_page():
    return Title("Home"), Main(
        # Hero Section
        Div(
            # Animated gradient background
            Div(style="""
                position: absolute;
                inset: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                opacity: 0.05;
                z-index: 0;
            """),
            
            # Content container
            Div(
                # Icon or logo
                Div(
                    "✨",
                    style="""
                        font-size: 64px;
                        margin-bottom: 20px;
                        animation: float 3s ease-in-out infinite;
                    """
                ),
                
                # Main heading with gradient text
                H1(
                    "Welcome to Reflection Manager",
                    style="""
                        font-size: clamp(32px, 5vw, 48px);
                        font-weight: 700;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                        margin-bottom: 16px;
                        line-height: 1.2;
                    """
                ),
                
                # Subtitle
                P(
                    "Capture your thoughts, track your growth, and reflect on your journey.",
                    style="""
                        font-size: 18px;
                        color: #64748b;
                        margin-bottom: 40px;
                        max-width: 500px;
                        line-height: 1.6;
                    """
                ),
                
                # CTA Button with hover effect
                A(
                    "Get Started →",
                    href="/reflections/",
                    style="""
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        padding: 16px 32px;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-decoration: none;
                        border-radius: 12px;
                        font-size: 16px;
                        font-weight: 600;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                        transition: all 0.3s ease;
                    """,
                    onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'",
                    onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'"
                ),
                
                style="""
                    position: relative;
                    z-index: 1;
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                """
            ),
            
            style="""
                position: relative;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 40px 20px;
            """
        ),
        
        # Global styles
        Style("""
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #ffffff;
                color: #1e293b;
                overflow-x: hidden;
            }
            
            @keyframes float {
                0%, 100% {
                    transform: translateY(0px);
                }
                50% {
                    transform: translateY(-20px);
                }
            }
            
            /* Responsive adjustments */
            @media (max-width: 640px) {
                body {
                    font-size: 14px;
                }
            }
        """),
        
        style="margin: 0;"
    )