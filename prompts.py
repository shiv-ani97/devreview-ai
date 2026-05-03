def get_prompt(language: str, focus: str, code: str, context: str) -> str:
    if focus == "security":
        return f"""You are a security expert reviewing {language} code for: {context}

Analyze ONLY security vulnerabilities. DO NOT report bugs or performance issues.

Code:
{code}

Find ONLY: SQL injection, hardcoded secrets, XSS, no input validation, exposed credentials.

Score between 1-10:
- SQL injection: -3 each
- Hardcoded secret/password/key: -2 each
- No input validation: -1
- Minimum score is 1

Return ONLY this JSON where bugs and performance_issues are ALWAYS empty arrays:
{{"summary":"security only summary","bugs":[],"security_issues":["issue1","issue2"],"performance_issues":[],"suggestions":["security fix 1","security fix 2","security fix 3"],"improved_code":"code with only security fixes applied using parameterized queries and env variables","score":2}}"""

    elif focus == "performance":
        return f"""You are a performance expert reviewing {language} code for: {context}

Analyze ONLY performance issues. DO NOT report security or bug issues.

Code:
{code}

Find ONLY: N+1 queries, repeated DB connections, inefficient loops, no caching, unnecessary computations.

Score between 1-10:
- N+1 query problem: -2 each
- New DB connection every call: -1.5
- Inefficient loop: -1 each
- No caching: -1
- Minimum score is 1

Return ONLY this JSON where bugs and security_issues are ALWAYS empty arrays:
{{"summary":"performance only summary","bugs":[],"security_issues":[],"performance_issues":["issue1","issue2"],"suggestions":["performance fix 1","performance fix 2","performance fix 3"],"improved_code":"code with only performance fixes applied using connection pooling and batch queries","score":5}}"""

    elif focus == "bugs":
        return f"""You are a bug detection expert reviewing {language} code for: {context}

Analyze ONLY bugs and logic errors. DO NOT report security or performance issues.

Code:
{code}

Find ONLY: missing error handling, unclosed connections, None not handled, logic errors, unhandled exceptions, missing edge cases.

Score between 1-10:
- No try/except: -2
- Unclosed connection: -1.5 each
- Missing null check: -1 each
- Logic error: -2 each
- Minimum score is 1

Return ONLY this JSON where security_issues and performance_issues are ALWAYS empty arrays:
{{"summary":"bugs only summary","bugs":["bug1","bug2","bug3"],"security_issues":[],"performance_issues":[],"suggestions":["bug fix 1","bug fix 2","bug fix 3"],"improved_code":"code with only bug fixes applied with proper error handling and closed connections","score":4}}"""

    else:
        return f"""You are a senior {language} engineer reviewing code for: {context}

Do a COMPLETE review covering ALL areas.

Code:
{code}

Find ALL issues:
- Bugs: missing error handling, unclosed connections, logic errors
- Security: SQL injection, hardcoded secrets, no input validation
- Performance: N+1 queries, inefficient loops, repeated connections

Score between 1-10:
- Critical security issue: -2 each
- Bug: -1.5 each
- Performance issue: -1 each
- Code quality: -0.5 each
- Minimum score is 1
- Maximum deduction is 9

Return ONLY this JSON with ALL sections filled:
{{"summary":"complete summary covering all issues found","bugs":["bug1","bug2"],"security_issues":["sec1","sec2"],"performance_issues":["perf1","perf2"],"suggestions":["fix1","fix2","fix3"],"improved_code":"fully fixed production ready code fixing ALL issues with comments","score":3}}"""