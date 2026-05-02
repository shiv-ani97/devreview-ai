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
    temperature=0.1
)

chain = REVIEW_PROMPT | llm | StrOutputParser()

async def review_code(code: str, language: str, focus: str) -> dict:
    try:
        result = await chain.ainvoke({
            "language": language,
            "focus": focus,
            "code": code
        })

        result = result.strip()

        # Try to extract JSON from response
        # Method 1: find ```json blocks
        if "```json" in result:
            result = result.split("```json")[1].split("```")[0].strip()
        # Method 2: find ``` blocks
        elif "```" in result:
            result = result.split("```")[1].split("```")[0].strip()
        # Method 3: find first { to last }
        else:
            match = re.search(r'\{.*\}', result, re.DOTALL)
            if match:
                result = match.group()

        return json.loads(result)

    except Exception as e:
        return {
            "summary": f"Code reviewed. Raw response parsing failed: {str(e)}",
            "bugs": ["Could not parse structured response"],
            "security_issues": [],
            "performance_issues": [],
            "suggestions": ["Try again or change focus type"],
            "improved_code": code,
            "score": 5
        }