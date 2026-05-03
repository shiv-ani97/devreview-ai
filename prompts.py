def get_review_prompt(language: str, focus: str, code: str, context: str) -> str:
    base_rules = """
STRICT RULES:
- Score must be integer 0-10 only, never higher
- Do NOT flag parameterized queries as SQL injection
- Do NOT flag os.environ.get() as hardcoded secret
- Do NOT flag JOIN as N+1 query
- Do NOT use placeholder text, be specific
- Flag returning str(e) to client as information leakage
- Never return passwords in SELECT * queries
"""

    if focus == "security":
        return f"""You are an elite Security Auditor reviewing {language} code for: {context}
{base_rules}
Analyze ONLY security vulnerabilities:
- SQL injection (string concatenation in queries)
- Hardcoded secrets/passwords/API keys
- Missing input validation
- Information leakage (returning raw exceptions)
- Password exposure in API responses

Score: Start 10. SQL injection: -3. Hardcoded secret: -2. No input validation: -1. Minimum 1.

Code:
{code}

Return ONLY this JSON:
{{"summary":"2-3 sentence professional security analysis","bugs":[],"security_issues":["specific issue 1","specific issue 2"],"performance_issues":[],"suggestions":["specific fix 1","specific fix 2","specific fix 3"],"improved_code":"","score":2}}"""

    elif focus == "performance":
        return f"""You are an elite Performance Architect reviewing {language} code for: {context}
{base_rules}
Analyze ONLY performance issues:
- N+1 queries (query inside loop, NOT a JOIN)
- New DB connection created every function call (no pooling)
- Inefficient loops
- Missing caching
- Thread safety issues with global connections

Score: Start 10. N+1 query: -2. New connection per call: -1.5. Inefficient loop: -1. No cache: -1. Minimum 1.

Code:
{code}

Return ONLY this JSON:
{{"summary":"2-3 sentence professional performance analysis","bugs":[],"security_issues":[],"performance_issues":["specific issue 1","specific issue 2"],"suggestions":["specific fix 1","specific fix 2","specific fix 3"],"improved_code":"","score":5}}"""

    elif focus == "bugs":
        return f"""You are an elite Bug Detection expert reviewing {language} code for: {context}
{base_rules}
Analyze ONLY bugs and logic errors:
- Missing try/except around database operations
- Unclosed database connections
- Missing None/null checks
- Returning raw exception strings str(e) to client
- Password hash exposed in SELECT * responses
- Missing return value handling

Score: Start 10. No try/except: -2. Unclosed connection: -1.5. Missing null check: -1. Logic error: -2. Minimum 1.

Code:
{code}

Return ONLY this JSON:
{{"summary":"2-3 sentence professional bug analysis","bugs":["specific bug with exact location","specific bug 2"],"security_issues":[],"performance_issues":[],"suggestions":["specific fix 1","specific fix 2","specific fix 3"],"improved_code":"","score":4}}"""

    else:
        return f"""You are a Senior Python Backend Architect reviewing {language} code for: {context}
{base_rules}
Do a COMPLETE review:
- Bugs: missing try/except, unclosed connections, null checks, str(e) leakage
- Security: SQL injection, hardcoded secrets, password exposure, input validation
- Performance: N+1 queries, connection pooling, inefficient loops

Score: Start 10. Critical security: -2. Bug: -1.5. Performance: -1. Minimum 1.

Code:
{code}

Return ONLY JSON no other text:
{{"summary":"2-3 sentence professional analysis","bugs":["specific bug"],"security_issues":["specific issue"],"performance_issues":["specific issue"],"suggestions":["fix1","fix2","fix3"],"improved_code":"","score":3}}"""


def get_fix_prompt(language: str, focus: str, code: str, context: str,
                   bugs: list, security_issues: list,
                   performance_issues: list, suggestions: list) -> str:

    issues_text = ""
    if bugs:
        issues_text += "\nBUGS TO FIX:\n" + "\n".join(f"- {b}" for b in bugs)
    if security_issues:
        issues_text += "\nSECURITY ISSUES TO FIX:\n" + "\n".join(f"- {s}" for s in security_issues)
    if performance_issues:
        issues_text += "\nPERFORMANCE ISSUES TO FIX:\n" + "\n".join(f"- {p}" for p in performance_issues)
    if suggestions:
        issues_text += "\nSUGGESTIONS TO IMPLEMENT:\n" + "\n".join(f"- {s}" for s in suggestions)

    focus_instruction = {
        "security": "Fix ONLY security issues. Use parameterized queries, os.environ.get() for secrets, input validation. Do NOT change performance code.",
        "performance": "Fix ONLY performance issues. Use connection pooling, JOIN queries, caching. Do NOT change security code.",
        "bugs": "Fix ONLY bugs. Add try/except/finally, close connections, add None checks. Do NOT change security code.",
        "general": "Fix ALL issues. Generate fully production-ready code."
    }.get(focus, "Fix all issues.")

    return f"""You are a Senior {language} Backend Architect.

Context: {context}
Task: {focus_instruction}

ORIGINAL CODE:
{code}

EXACT ISSUES TO FIX:
{issues_text}

STRICT RULES FOR OPTIMIZED CODE:
- Implement EVERY suggestion listed above
- Never return password hashes in API responses
- Never expose raw exception strings str(e) to client
- Use parameterized queries for ALL database operations
- Add proper logging instead of print statements
- Each fix must have a comment explaining what was fixed and why
- Code must score 9/10 when reviewed again
- Return ONLY complete {language} code, no markdown, no backticks"""