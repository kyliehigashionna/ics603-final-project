from fasthtml.common import FastHTML
from pages.home_page import home_page
from pages.reflections_page import reflections_page
from components.add_reflection import create_reflection
from services.recommendation_service import get_recommendation
app = FastHTML()

@app.get("/")
async def home():
    return await home_page() 


@app.get("/reflections/")
async def reflections(tab: str = "add", id: int = None, user_id: str = None, query: str = ""):
    return await reflections_page(tab, id, user_id, query)


@app.post("/reflections/create")
async def create(title: str, text: str, user_id: int):
    return await create_reflection(title, text, user_id)


@app.post("/reflections/recommend")
async def recommend(user_id: int, context: str, prompt: str):
    # Get the recommendation result
    result = await get_recommendation(user_id, context, prompt)
    
    # Create the recommendation data
    recommendation_data = {
        "user_id": user_id,
        "context": context,
        "prompt": prompt,
        "recommendation": result["recommendation"],
        "reflections_used": result["reflections_used"]
    }
    
    # Return the full page with the results
    return await reflections_page(
        tab="recommendations",
        recommendation_data=recommendation_data
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)