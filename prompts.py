from langchain_core.prompts import PromptTemplate

REVIEW_PROMPT = PromptTemplate(
    input_variables=["language", "focus", "code"],
    template="""You are an expert {language} code reviewer.

IMPORTANT: You must respond with ONLY a JSON object. No explanations, no markdown, no text before or after. Just pure JSON.

Focus area: {focus}

Code to review:
{code}

Return ONLY this JSON, nothing else:
{{"summary": "brief overall summary here","bugs": ["bug description 1", "bug description 2"],"security_issues": ["security issue 1"],"performance_issues": ["performance issue 1"],"suggestions": ["suggestion 1", "suggestion 2"],"improved_code": "full improved code here","score": 7}}"""
)