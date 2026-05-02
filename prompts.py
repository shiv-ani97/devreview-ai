from langchain_core.prompts import PromptTemplate

REVIEW_PROMPT = PromptTemplate(
    input_variables=["language", "focus", "code"],
    template="""Review this {language} code. Focus on: {focus}.

Code:
{code}

Reply with ONLY this JSON and nothing else:
{{"summary":"summary here","bugs":["bug1","bug2"],"security_issues":["issue1"],"performance_issues":["issue1"],"suggestions":["fix1","fix2"],"improved_code":"fixed code here","score":5}}"""
)