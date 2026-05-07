import os
import json
import re
from dotenv import load_dotenv
from groq import AsyncGroq
from prompts import get_review_prompt

load_dotenv()
client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_json(text: str):
    try:
        return json.loads(text)
    except:
        pass
    if "```json" in text:
        try:
            return json.loads(text.split("```json")[1].split("```")[0].strip())
        except:
            pass
    if "```" in text:
        try:
            return json.loads(text.split("```")[1].split("```")[0].strip())
        except:
            pass
    try:
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

async def review_code(code: str, language: str, focus: str, context: str) -> dict:
    try:
        review_prompt = get_review_prompt(language, focus, code, context)
        response = await client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a strict code reviewer. Respond with ONLY valid JSON. No text before or after."},
                {"role": "user", "content": review_prompt}
            ],
            temperature=0.0,
            max_tokens=1500
        )
        result = response.choices[0].message.content.strip()
        parsed = extract_json(result)

        if parsed:
            return {
                "summary": str(parsed.get("summary") or "Review complete"),
                "bugs": parsed.get("bugs") or [],
                "security_issues": parsed.get("security_issues") or [],
                "performance_issues": parsed.get("performance_issues") or [],
                "suggestions": parsed.get("suggestions") or [],
                "improved_code": "",
                "score": max(1, min(10, int(parsed.get("score") or 5)))
            }

        return {
            "summary": "Could not parse response. Please try again.",
            "bugs": [], "security_issues": [], "performance_issues": [],
            "suggestions": ["Try again"], "improved_code": "", "score": 5
        }

    except Exception as e:
        return {
            "summary": f"Error: {str(e)}",
            "bugs": [], "security_issues": [], "performance_issues": [],
            "suggestions": ["Try again"], "improved_code": "", "score": 5
        }