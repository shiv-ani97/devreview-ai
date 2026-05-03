def get_prompt(language: str, focus: str, code: str, context: str) -> str:
    if focus == "security":
        return f"""You are a security expert reviewing {language} code for: {context}

Analyze ONLY security vulnerabilities. DO NOT report bugs or performance issues.

Code:
{code}

Step 1 - Find ONLY these security issues:
- SQL injection (string concatenation in queries)
- Hardcoded secrets/passwords/API keys
- Missing input validation
- Exposed credentials

Step 2 - Score between 1-10:
- SQL injection: -3 each
- Hardcoded secret: -2 each
- No input validation: -1
- Minimum score is 1

Step 3 - Generate improved_code by applying EACH suggestion you found:
- For EVERY SQL injection found: replace with parameterized query using ? placeholder
- For EVERY hardcoded secret found: replace with os.environ.get('SECRET_NAME')
- For EVERY missing input validation: add if not username or not password validation
- Add import os at top if using env variables
- The improved_code must directly address ALL security_issues listed
- Do NOT change performance or error handling code

Return ONLY this JSON:
{{"summary":"2 sentence security summary for {context}","bugs":[],"security_issues":["specific issue 1","specific issue 2"],"performance_issues":[],"suggestions":["specific security fix 1","specific security fix 2","specific security fix 3"],"improved_code":"complete code with ALL security fixes applied based on suggestions","score":2}}"""

    elif focus == "performance":
        return f"""You are a performance expert reviewing {language} code for: {context}

Analyze ONLY performance issues. DO NOT report security or bug issues.

Code:
{code}

Step 1 - Find ONLY these performance issues:
- N+1 query problem (query inside loop)
- New DB connection created on every function call
- Inefficient loops that could use better algorithms
- Missing caching for repeated expensive calls

Step 2 - Score between 1-10:
- N+1 query: -2 each
- New DB connection every call: -1.5
- Inefficient loop: -1 each
- No caching: -1
- Minimum score is 1

Step 3 - Generate improved_code by applying EACH suggestion:
- For N+1 query: rewrite using JOIN to fetch all data in ONE query
- For repeated connections: accept conn as function parameter or use connection pool
- For inefficient loops: use list comprehension or batch operations
- For missing cache: add @functools.lru_cache or simple dict cache
- The improved_code must directly address ALL performance_issues listed
- Do NOT change security related code

Return ONLY this JSON:
{{"summary":"2 sentence performance summary for {context}","bugs":[],"security_issues":[],"performance_issues":["specific issue 1","specific issue 2"],"suggestions":["specific performance fix 1","specific performance fix 2","specific performance fix 3"],"improved_code":"complete code with ALL performance fixes applied based on suggestions","score":3}}"""

    elif focus == "bugs":
        return f"""You are a bug detection expert reviewing {language} code for: {context}

Analyze ONLY bugs and logic errors. DO NOT report security or performance issues.

Code:
{code}

Step 1 - Find ONLY these bugs:
- Missing try/except around database operations
- Unclosed database connections (no conn.close() or finally block)
- Missing None/null checks before using variables
- Logic errors and unhandled edge cases
- Missing return value handling

Step 2 - Score between 1-10:
- No try/except: -2
- Unclosed connection: -1.5 each
- Missing null check: -1 each
- Logic error: -2 each
- Minimum score is 1

Step 3 - Generate improved_code by applying EACH suggestion:
- For missing try/except: wrap ALL DB operations in try/except/finally
- For unclosed connections: add conn.close() in finally block
- For missing None checks: add if user is None or if result is None checks
- For logic errors: fix the specific logic issue found
- For missing edge cases: add proper handling
- The improved_code must directly fix ALL bugs listed
- Do NOT change security related code

Return ONLY this JSON:
{{"summary":"2 sentence bug summary for {context}","bugs":["specific bug 1","specific bug 2"],"security_issues":[],"performance_issues":[],"suggestions":["specific bug fix 1","specific bug fix 2","specific bug fix 3"],"improved_code":"complete code with ALL bug fixes applied based on suggestions","score":4}}"""

    else:
        return f"""You are a senior {language} engineer reviewing code for: {context}

Code:
{code}

Step 1 - Find ALL issues:
- Bugs: missing try/except, unclosed connections, null checks
- Security: SQL injection, hardcoded secrets, no input validation
- Performance: N+1 queries, repeated connections, no caching

Step 2 - Score between 1-10:
- Critical security: -2 each
- Bug: -1.5 each
- Performance: -1 each
- Minimum score 1

Step 3 - Generate improved_code that fixes EVERYTHING found:
- Fix ALL SQL injections with parameterized queries
- Move ALL secrets to os.environ.get()
- Add try/except/finally around ALL DB operations
- Fix N+1 queries with JOIN
- Add input validation
- The improved code must score 9/10 if reviewed again

Reply with ONLY JSON no other text:
{{"summary":"summary","bugs":["bug1"],"security_issues":["sec1"],"performance_issues":["perf1"],"suggestions":["fix1","fix2","fix3"],"improved_code":"production ready code fixing ALL issues","score":3}}"""