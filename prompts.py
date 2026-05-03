def get_prompt(language: str, focus: str, code: str, context: str) -> str:
    
    focus_instructions = {
        "general": "Review everything - bugs, security, performance, code quality.",
        "security": "ONLY look for security issues: SQL injection, hardcoded secrets, XSS, authentication flaws, exposed credentials. Leave bugs and performance_issues as empty arrays.",
        "performance": "ONLY look for performance issues: slow queries, memory leaks, inefficient loops, missing caching. Leave bugs and security_issues as empty arrays.",
        "bugs": "ONLY look for bugs: logic errors, null pointer issues, missing error handling, edge cases. Leave security_issues and performance_issues as empty arrays."
    }

    instruction = focus_instructions.get(focus, focus_instructions["general"])

    scoring = ""
    if focus == "security":
        scoring = """
Security scoring rules:
- Start at 10
- SQL injection found: -3 points each
- Hardcoded password/secret/key: -2 points each  
- No input validation: -1 point
- Missing authentication: -2 points
- Code with SQL injection must score maximum 4/10
- Code with hardcoded secrets must score maximum 5/10"""
    elif focus == "performance":
        scoring = """
Performance scoring rules:
- Start at 10
- N+1 query problem: -2 points
- Missing database indexes: -1 point
- No caching for repeated calls: -1 point
- Inefficient loop or algorithm: -1.5 points"""
    elif focus == "bugs":
        scoring = """
Bug scoring rules:
- Start at 10
- Critical bug that causes crashes: -2.5 points
- Missing error handling: -1.5 points
- Logic error: -1.5 points
- Edge case not handled: -1 point"""
    else:
        scoring = """
General scoring:
- Start at 10, deduct for all issue types found
- Critical issues: -2 points each
- Medium issues: -1 point each
- Minor issues: -0.5 points each"""

    return f"""You are a senior {language} engineer reviewing code for a {context}.

Task: {instruction}
{scoring}

Code to review:
```{language}
{code}
```

Return a JSON object with these exact keys:
- summary: string (2-3 sentences about what you found, specific to {focus})
- bugs: array of strings (empty [] if focus is not bugs or general)
- security_issues: array of strings (empty [] if focus is not security or general)  
- performance_issues: array of strings (empty [] if focus is not performance or general)
- suggestions: array of 3 specific actionable fixes for {focus} issues
- improved_code: string (rewrite fixing ONLY the {focus} issues found, with comments)
- score: integer from 1-10 based on scoring rules above
"""