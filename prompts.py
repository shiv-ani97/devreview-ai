from langchain_core.prompts import PromptTemplate

REVIEW_PROMPT = PromptTemplate(
    input_variables=["language", "focus", "code", "context"],
    template="""You are a senior {language} engineer. A developer needs help with their code.

Developer's context: {context}
Review focus: {focus}
Language: {language}

Code to review:
{code}

Instructions:
- ONLY report issues related to the focus area "{focus}"
- If focus is "security": only report security_issues, leave bugs and performance_issues as empty lists
- If focus is "performance": only report performance_issues, leave bugs and security_issues as empty lists  
- If focus is "bugs": only report bugs, leave security_issues and performance_issues as empty lists
- If focus is "general": report everything
- improved_code must fix ONLY the issues related to "{focus}"
- Base your suggestions on the developer's context

Reply with ONLY this JSON:
{{"summary":"2 sentence summary","bugs":[],"security_issues":[],"performance_issues":[],"suggestions":["specific fix 1","specific fix 2"],"improved_code":"optimized code here","score":5}}"""
)