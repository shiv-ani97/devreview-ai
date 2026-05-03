import os
import json
import re
from dotenv import load_dotenv
from groq import AsyncGroq
from prompts import get_prompt

load_dotenv()

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

async def review_code(code: str, language: str, focus: str, context: str) -> dict:
    try:
        prompt = get_prompt(language, focus, code, context)
        
        response = await client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict code reviewer. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        result = response.choices[0].message.content
        return json.loads(result)

    except Exception as e:
        return {
            "summary": f"Error: {str(e)}",
            "bugs": [],
            "security_issues": [],
            "performance_issues": [],
            "suggestions": ["Try again"],
            "improved_code": code,
            "score": 5
        }