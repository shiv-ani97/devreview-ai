def get_review_prompt(language: str, focus: str, code: str, context: str) -> str:
    base_rules = """
STRICT RULES - NEVER VIOLATE:
- Score 0-10 only, never higher or negative
- Do NOT flag parameterized queries (? or %s) as SQL injection
- Do NOT flag os.environ.get() as hardcoded secret
- Do NOT flag JOIN or subquery as N+1 query
- Do NOT flag bcrypt as bad practice
- Do NOT flag logging.error() as information leakage
- Do NOT flag custom error messages like {'error': 'message'} as information leakage
- ONLY flag str(e) returned directly to client as information leakage
- If code uses try/except/finally properly do NOT flag missing error handling
- If code uses parameterized queries do NOT flag SQL injection
- If code uses os.environ.get() do NOT flag hardcoded secrets
- If code already fixes an issue do NOT flag that issue
- Be honest — if code is good give it 8-9/10
- Only deduct points for REAL issues that actually exist in the code
"""

    if focus == "security":
        return f"""You are an elite Security Auditor reviewing {language} code for: {context}
{base_rules}
Analyze ONLY security vulnerabilities:
- SQL injection (string concatenation in queries only)
- Hardcoded secrets (literal strings only, not os.environ.get)
- Missing input validation
- str(e) returned directly to client
- Password hash exposed in API response

Score: Start 10. SQL injection: -3. Hardcoded secret: -2. No input validation: -1. Minimum 1.

Code:
{code}

Return ONLY this JSON:
{{"summary":"2-3 sentence professional security analysis of actual issues found","bugs":[],"security_issues":["specific real issue 1","specific real issue 2"],"performance_issues":[],"suggestions":["specific fix 1","specific fix 2","specific fix 3"],"improved_code":"","score":2}}"""

    elif focus == "performance":
        return f"""You are an elite Performance Architect reviewing {language} code for: {context}
{base_rules}
Analyze ONLY performance issues:
- N+1 queries (query inside loop only, NOT a JOIN or subquery)
- New DB connection created every function call with no pooling
- Inefficient loops that could use better algorithms
- Missing caching for repeated expensive calls
- Thread safety issues with global connections

Score: Start 10. N+1 query: -2. New connection per call: -1.5. Inefficient loop: -1. No cache: -1. Minimum 1.

Code:
{code}

Return ONLY this JSON:
{{"summary":"2-3 sentence professional performance analysis of actual issues found","bugs":[],"security_issues":[],"performance_issues":["specific real issue 1","specific real issue 2"],"suggestions":["specific fix 1","specific fix 2","specific fix 3"],"improved_code":"","score":5}}"""

    elif focus == "bugs":
        return f"""You are an elite Bug Detection expert reviewing {language} code for: {context}
{base_rules}
Analyze ONLY bugs and logic errors:
- Missing try/except around database operations
- Unclosed database connections (no finally block)
- Functions defined inside try block (syntax/logic error)
- Missing None/null checks
- str(e) returned directly to client
- Password hash exposed in SELECT * response

Score: Start 10. No try/except: -2. Unclosed connection: -1.5. Missing null check: -1. Logic error: -2. Minimum 1.

Code:
{code}

Return ONLY this JSON:
{{"summary":"2-3 sentence professional bug analysis of actual issues found","bugs":["specific real bug 1","specific real bug 2"],"security_issues":[],"performance_issues":[],"suggestions":["specific fix 1","specific fix 2","specific fix 3"],"improved_code":"","score":4}}"""

    else:
        return f"""You are a Senior {language} Backend Architect reviewing code for: {context}
{base_rules}
Do a COMPLETE honest review:
- Bugs: missing try/except, unclosed connections, null checks, functions inside try blocks
- Security: SQL injection (string concat only), hardcoded secrets (literals only), password exposure
- Performance: N+1 queries (loop only), connection pooling, inefficient loops

Score: Start 10. Critical security: -2. Bug: -1.5. Performance: -1. Minimum 1.
If code is already well written give it 7-9/10 honestly.

Code:
{code}

Return ONLY JSON no other text:
{{"summary":"2-3 sentence honest professional analysis","bugs":["specific bug"],"security_issues":["specific issue"],"performance_issues":["specific issue"],"suggestions":["fix1","fix2","fix3"],"improved_code":"","score":3}}"""


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

    if not issues_text.strip():
        issues_text = "No major issues found. Code is already well written."

    focus_instruction = {
        "security": "Fix ONLY security issues listed. Use parameterized queries, os.environ.get() for secrets, input validation. Do NOT change performance or bug-related code.",
        "performance": "Fix ONLY performance issues listed. Use connection pooling, JOIN queries, caching. Do NOT change security code.",
        "bugs": "Fix ONLY bugs listed. Add try/except/finally, close connections in finally, add None checks. Do NOT change security code.",
        "general": "Fix ALL issues listed. Generate fully production-ready code."
    }.get(focus, "Fix all issues listed.")

    return f"""You are a Senior {language} Backend Architect.

Context: {context}
Task: {focus_instruction}

ORIGINAL CODE:
{code}

EXACT ISSUES FOUND AND FIXES REQUIRED:
{issues_text}

STRICT RULES FOR OPTIMIZED CODE:
- NEVER define functions inside a try/except block
- NEVER close connection at module level
- Each function must create its own connection and close it in finally block
- Use threading.local() for thread-safe connections if needed
- Never return password hash in any response — exclude from SELECT or delete from dict
- Never expose raw str(e) to client — use logging.error() and return custom message
- Use parameterized queries for ALL database operations
- Add proper logging with logging module not print statements
- Add type hints to all functions
- Each fix must have a comment explaining what was fixed and why
- If no issues found write clean optimized version of the same code
- Code must score 8-9/10 when reviewed again
- Return ONLY complete {language} code, no markdown, no backticks, no explanations"""