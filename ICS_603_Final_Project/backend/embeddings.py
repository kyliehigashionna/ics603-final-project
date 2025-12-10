from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def embed_text(text: str):
    response = await asyncio.to_thread(lambda: client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    ))
    return response.data[0].embedding