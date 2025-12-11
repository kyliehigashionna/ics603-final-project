"""
Recommendation generation using RAG
"""
from pydantic_ai import Agent, RunContext
from typing import List, Dict, Any
from dotenv import load_dotenv


load_dotenv()

recommendation_agent = Agent(
    "openai:gpt-4o-mini",
    system_prompt="""You are a helpful assistant that provides personalized recommendations 
    based on a user's past reflections. 
    
    You have access to a tool called `analyze_topics` which analyzes the user's
    reflection topics, identifies dominant themes, and provides insight into what
    the user cares about most.
    
    Use the context from their reflections to give 
    thoughtful, relevant recommendations that align with their interests and experiences.""",
)

@recommendation_agent.tool
async def analyze_topics(ctx: RunContext[List[Dict]]) -> Dict[str, Any]:
    """Analyze user reflection topics for deeper RAG personalization."""
    counts = {}
    for reflection in ctx.deps:
        for topic in reflection.get("topics", []):
            counts[topic] = counts.get(topic, 0) + 1

    if not counts:
        return {
            "counts": {},
            "top_topic": None,
            "insight": "The user has no topics recorded."
        }

    top_topic = max(counts, key=counts.get)
    print("analyze_topics tool called! Output:", counts, top_topic)
    return {
        "counts": counts,
        "top_topic": top_topic,
        "insight": (
            f"""The user writes most about '{top_topic}', suggesting it is a 
            major interest, concern, or recurring emotional theme in their life."""
        )
    }

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
    Before doing so, you can call the `analyze_topics` tool to understand what topics the 
    user cares about most.
    """
    
    result = await recommendation_agent.run(
        user_prompt,
        deps=reflections
    )
    return result.output
