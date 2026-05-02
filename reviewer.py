import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts import REVIEW_PROMPT

load_dotenv()

llm = ChatGroq(
    api_key=os.environ.get("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.0
)

chain = REVIEW_PROMPT | llm | StrOutputParser()

def extract_json(text: str) -> dict:
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
        result = await chain.ainvoke({
            "language": language,
            "focus": focus,
            "code": code,
            "context": context
        })
        parsed = extract_json(result.strip())
        if parsed:
            return parsed
        return {
            "summary": "Parsing failed. Please try again.",
            "bugs": [],
            "security_issues": [],
            "performance_issues": [],
            "suggestions": ["Try again"],
            "improved_code": code,
            "score": 5
        }
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