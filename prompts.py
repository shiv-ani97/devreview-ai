def get_review_prompt(language: str, focus: str, code: str, context: str) -> str:
    if focus == "security":
        return f"""Review this {language} code for security issues only. Context: {context}

Code:
{code}

Find ONLY: SQL injection, hardcoded secrets, missing input validation, exposed credentials.
Score 1-10. SQL injection: -3 each. Hardcoded secret: -2 each. Input validation missing: -1. Minimum 1.

Return ONLY JSON:
{{"summary":"security summary","bugs":[],"security_issues":["issue1","issue2"],"performance_issues":[],"suggestions":["fix1","fix2","fix3"],"improved_code":"","score":2}}"""

    elif focus == "performance":
        return f"""Review this {language} code for performance issues only. Context: {context}

Code:
{code}

Find ONLY: N+1 queries, repeated DB connections, inefficient loops, missing caching.
Score 1-10. N+1 query: -2 each. New connection per call: -1.5. Inefficient loop: -1. No cache: -1. Minimum 1.

Return ONLY JSON:
{{"summary":"performance summary","bugs":[],"security_issues":[],"performance_issues":["issue1","issue2"],"suggestions":["fix1","fix2","fix3"],"improved_code":"","score":5}}"""

    elif focus == "bugs":
        return f"""Review this {language} code for bugs only. Context: {context}

Code:
{code}

Find ONLY: missing try/except, unclosed connections, None not handled, logic errors.
Score 1-10. No try/except: -2. Unclosed connection: -1.5. Missing null check: -1. Logic error: -2. Minimum 1.

Return ONLY JSON:
{{"summary":"bug summary","bugs":["bug1","bug2"],"security_issues":[],"performance_issues":[],"suggestions":["fix1","fix2","fix3"],"improved_code":"","score":4}}"""

    else:
        return f"""Review this {language} code completely. Context: {context}

Code:
{code}

Find ALL issues: bugs, security vulnerabilities, performance problems.
Score 1-10. Critical security: -2 each. Bug: -1.5 each. Performance: -1 each. Minimum 1.

Return ONLY JSON:
{{"summary":"complete summary","bugs":["bug1"],"security_issues":["sec1"],"performance_issues":["perf1"],"suggestions":["fix1","fix2","fix3"],"improved_code":"","score":3}}"""


def get_fix_prompt(language: str, focus: str, code: str, context: str,
                   bugs: list, security_issues: list,
                   performance_issues: list, suggestions: list) -> str:

    issues_text = ""
    if bugs:
        issues_text += f"\nBUGS TO FIX:\n" + "\n".join(f"- {b}" for b in bugs)
    if security_issues:
        issues_text += f"\nSECURITY ISSUES TO FIX:\n" + "\n".join(f"- {s}" for s in security_issues)
    if performance_issues:
        issues_text += f"\nPERFORMANCE ISSUES TO FIX:\n" + "\n".join(f"- {p}" for p in performance_issues)
    if suggestions:
        issues_text += f"\nSUGGESTIONS TO IMPLEMENT:\n" + "\n".join(f"- {s}" for s in suggestions)

    focus_instruction = {
        "security": "Fix ONLY the security issues listed. Do NOT change performance or bug-related code.",
        "performance": "Fix ONLY the performance issues listed. Do NOT change security or bug-related code.",
        "bugs": "Fix ONLY the bugs listed. Do NOT change security or performance-related code.",
        "general": "Fix ALL issues listed. Generate fully production-ready code."
    }.get(focus, "Fix all issues listed.")

    return f"""You are an expert {language} developer. 

Context: This is a {context}.
{focus_instruction}

ORIGINAL CODE:
{code}

ISSUES FOUND AND FIXES REQUIRED:
{issues_text}

INSTRUCTIONS:
- Apply EVERY fix listed in suggestions above to the original code
- Each suggestion must be directly implemented in the code
- Add comments explaining each fix you made
- The fixed code must score 9/10 when reviewed again
- Return ONLY the complete fixed {language} code
- No explanations, no markdown, just the code"""