import os
import json
import re
from dotenv import load_dotenv
from groq import AsyncGroq
from prompts import get_review_prompt, get_fix_prompt

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

async def call_llm(prompt: str, system: str) -> str:
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()

async def review_code(code: str, language: str, focus: str, context: str) -> dict:
    try:
        # Call 1: Find issues and suggestions
        review_prompt = get_review_prompt(language, focus, code, context)
        review_result = await call_llm(
            review_prompt,
            "You are a strict code reviewer. Respond with ONLY valid JSON. No text before or after."
        )
        parsed = extract_json(review_result)

        if not parsed:
            return {
                "summary": "Could not parse response. Please try again.",
                "bugs": [], "security_issues": [], "performance_issues": [],
                "suggestions": ["Try again"], "improved_code": code, "score": 5
            }

        # Extract suggestions and issues from first call
        suggestions = parsed.get("suggestions", [])
        bugs = parsed.get("bugs", [])
        security_issues = parsed.get("security_issues", [])
        performance_issues = parsed.get("performance_issues", [])
        score = parsed.get("score", 5)
        summary = parsed.get("summary", "")

        # Call 2: Generate optimal code based on exact issues found
        fix_prompt = get_fix_prompt(
            language=language,
            focus=focus,
            code=code,
            context=context,
            bugs=bugs,
            security_issues=security_issues,
            performance_issues=performance_issues,
            suggestions=suggestions
        )
        fixed_code = await call_llm(
            fix_prompt,
            "You are an expert code optimizer. Return ONLY the fixed code, no explanations, no markdown, no backticks."
        )

        # Clean code response
        if "```" in fixed_code:
            fixed_code = fixed_code.split("```")[1].split("```")[0].strip()
            if fixed_code.startswith(language):
                fixed_code = fixed_code[len(language):].strip()

        return {
            "summary": summary,
            "bugs": bugs,
            "security_issues": security_issues,
            "performance_issues": performance_issues,
            "suggestions": suggestions,
            "improved_code": fixed_code,
            "score": score
        }

    except Exception as e:
        return {
            "summary": f"Error: {str(e)}",
            "bugs": [], "security_issues": [], "performance_issues": [],
            "suggestions": ["Try again"], "improved_code": code, "score": 5
        }