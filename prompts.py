def get_prompt(language: str, focus: str, code: str, context: str) -> str:
    if focus == "security":
        return f"""You are a security expert reviewing {language} code for: {context}

Analyze ONLY security vulnerabilities in this code:
{code}

Find: SQL injection, hardcoded secrets, XSS, no input validation, exposed credentials.

Scoring: Start at 10. SQL injection: -3 each. Hardcoded secret: -2 each. No input validation: -1.

Return ONLY this JSON:
{{"summary":"security summary","bugs":[],"security_issues":["issue1","issue2"],"performance_issues":[],"suggestions":["fix1","fix2","fix3"],"improved_code":"fixed code here","score":3}}"""

    elif focus == "performance":
        return f"""You are a performance expert reviewing {language} code for: {context}

Analyze ONLY performance issues in this code:
{code}

Find: N+1 queries, repeated DB connections, inefficient loops, no caching.

Scoring: Start at 10. N+1 query: -2 each. New DB connection every call: -1.5. Inefficient loop: -1 each.

Return ONLY this JSON:
{{"summary":"performance summary","bugs":[],"security_issues":[],"performance_issues":["issue1","issue2"],"suggestions":["fix1","fix2","fix3"],"improved_code":"fixed code here","score":5}}"""

    elif focus == "bugs":
        return f"""You are a bug detection expert reviewing {language} code for: {context}

Analyze ONLY bugs and logic errors in this code:
{code}

Find: missing error handling, unclosed connections, null not handled, logic errors, unhandled exceptions.

Scoring: Start at 10. No try/except: -2. Unclosed connection: -1.5 each. Logic error: -2 each.

Return ONLY this JSON:
{{"summary":"bug summary","bugs":["bug1","bug2"],"security_issues":[],"performance_issues":[],"suggestions":["fix1","fix2","fix3"],"improved_code":"fixed code here","score":5}}"""

    else:
        return f"""You are a senior {language} engineer reviewing code for: {context}

Do a COMPLETE review of this code:
{code}

Find ALL issues - bugs, security vulnerabilities, performance problems.

Scoring: Start at 10. Critical security: -2.5 each. Bug: -1.5 each. Performance: -1 each.

Return ONLY this JSON:
{{"summary":"complete summary","bugs":["bug1"],"security_issues":["sec1"],"performance_issues":["perf1"],"suggestions":["fix1","fix2","fix3"],"improved_code":"fully fixed production code here","score":3}}"""