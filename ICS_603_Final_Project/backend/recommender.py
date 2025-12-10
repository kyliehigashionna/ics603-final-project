"""
Recommendation generation using RAG
"""
from pydantic_ai import Agent
from typing import List, Dict
from dotenv import load_dotenv


load_dotenv()

recommendation_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="""You are a helpful assistant that provides personalized recommendations 
    based on a user's past reflections. Use the context from their reflections to give 
    thoughtful, relevant recommendations that align with their interests and experiences.""",
)

async def generate_recommendation(
    prompt: str, 
    context: str, 
    reflections: List[Dict]
) -> str:
    """Generate a recommendation based on user reflections"""
    
    # Format reflections as context
    reflection_context = "\n\n".join([
        f"Reflection: {r['title']}\n{r['text']}\nTopics: {', '.join(r['topics'])}"
        for r in reflections
    ])
    
    user_prompt = f"""
    Based on the following context about what the user wants to know:
    {context}
    
    Here are some relevant reflections from the user:
    
    {reflection_context}
    
    User's request: {prompt}
    
    Please provide a personalized recommendation based on their reflections and interests.
    """
    
    result = await recommendation_agent.run(user_prompt)
    return result.output
