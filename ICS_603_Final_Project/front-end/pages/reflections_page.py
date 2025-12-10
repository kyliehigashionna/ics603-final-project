from fasthtml.common import *
from components.add_reflection import add_reflection_form
from components.view_reflections import view_reflections
from components.single_reflection import single_reflection
from components.search_reflections import search_reflections
from components.recommendations import recommendations_form

async def reflections_page(tab: str = "add", id: int = None, user_id: str = None, query: str = "", recommendation_data: dict = None):
    selected_user_id = None
    if user_id and user_id != "all":
        selected_user_id = int(user_id)
    
    tabs = Div(
        A("Home", href="/", title="Home",
          style="padding: 10px 20px; border: 1px solid #ccc; text-decoration: none; background: #f0f0f0; color: #333;"),
        A("Add Reflection", href="/reflections/?tab=add", 
          style=f"padding: 10px 20px; border: 1px solid #ccc; text-decoration: none; {'background: #007bff; color: white;' if tab == 'add' and not id else 'background: #f0f0f0; color: #333;'}"),
        A("View Reflections", href="/reflections/?tab=view", 
          style=f"padding: 10px 20px; border: 1px solid #ccc; text-decoration: none; {'background: #007bff; color: white;' if tab == 'view' or id else 'background: #f0f0f0; color: #333;'}"),
        A("Search", href="/reflections/?tab=search",
          style=f"padding: 10px 20px; border: 1px solid #ccc; text-decoration: none; {'background: #007bff; color: white;' if tab == 'search' else 'background: #f0f0f0; color: #333;'}"),
        A("Recommendations", href="/reflections/?tab=recommendations",
          style=f"padding: 10px 20px; border: 1px solid #ccc; text-decoration: none; {'background: #007bff; color: white;' if tab == 'recommendations' else 'background: #f0f0f0; color: #333;'}"),
        style="margin-bottom: 20px;"
    )
    
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
        content = await search_reflections(search_query=query, selected_user_id=selected_user_id)
    else:
        content = await view_reflections(selected_user_id)
    
    return Title("Reflections"), Main(tabs, content)