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

For improved_code you MUST:
- Replace ALL string concatenation queries with parameterized queries using ? placeholders
- Move ALL hardcoded secrets to os.environ.get()
- Add input validation for ALL user inputs
- The improved code must score 9/10 if reviewed again
- Do NOT change performance or error handling code

Return ONLY this JSON where bugs and performance_issues are ALWAYS empty arrays:
{{"summary":"security only summary","bugs":[],"security_issues":["issue1","issue2"],"performance_issues":[],"suggestions":["fix1","fix2","fix3"],"improved_code":"fully secure code here that would score 9/10","score":2}}"""

    elif focus == "performance":
        return f"""You are a performance expert reviewing {language} code for: {context}

Analyze ONLY performance issues. DO NOT report security or bug issues.

Code:
{code}

Find ONLY: N+1 queries, repeated DB connections, inefficient loops, no caching.

Score between 1-10:
- N+1 query problem: -2 each
- New DB connection every call: -1.5
- Inefficient loop: -1 each
- No caching: -1
- Minimum score is 1

For improved_code you MUST:
- Fix N+1 queries by using JOIN to fetch all data in single query
- Use connection pooling or pass connection as parameter instead of creating new connection every call
- Replace inefficient loops with optimized queries
- Add caching using functools.lru_cache or dict for repeated calls
- The improved code must score 9/10 if reviewed again for performance
- Do NOT change security related code

Return ONLY this JSON where bugs and security_issues are ALWAYS empty arrays:
{{"summary":"performance only summary","bugs":[],"security_issues":[],"performance_issues":["issue1","issue2"],"suggestions":["fix1","fix2","fix3"],"improved_code":"fully optimized code here that would score 9/10","score":3}}"""

    elif focus == "bugs":
        return f"""You are a bug detection expert reviewing {language} code for: {context}

Analyze ONLY bugs and logic errors. DO NOT report security or performance issues.

Code:
{code}

Find ONLY: missing error handling, unclosed connections, None not handled, logic errors, unhandled exceptions.

Score between 1-10:
- No try/except: -2
- Unclosed connection: -1.5 each
- Missing null check: -1 each
- Logic error: -2 each
- Minimum score is 1

For improved_code you MUST:
- Wrap ALL database operations in try/except/finally blocks
- Close ALL connections in finally block to prevent leaks
- Add None/null checks before using any variable
- Handle ALL edge cases and exceptions properly
- Return meaningful error messages instead of None
- The improved code must score 9/10 if reviewed again for bugs
- Do NOT change security related code

Return ONLY this JSON where security_issues and performance_issues are ALWAYS empty arrays:
{{"summary":"bugs only summary","bugs":["bug1","bug2"],"security_issues":[],"performance_issues":[],"suggestions":["fix1","fix2","fix3"],"improved_code":"fully bug-free code here that would score 9/10","score":4}}"""

    else:
        return f"""You are a senior {language} engineer reviewing code for: {context}

Do a COMPLETE review covering ALL areas.

Code:
{code}

Find ALL issues - bugs, security vulnerabilities, performance problems.

Score between 1-10:
- Critical security issue: -2 each
- Bug: -1.5 each
- Performance issue: -1 each
- Minimum score is 1

For improved_code you MUST fix ALL of these:
1. Replace string concatenation queries with parameterized queries
2. Move hardcoded secrets to os.environ.get()
3. Add try/except/finally blocks around all DB operations
4. Close connections in finally blocks
5. Fix N+1 queries using JOIN
6. Add input validation
7. Add proper error handling and return meaningful responses
8. The improved code must score 9/10 if reviewed again

Return ONLY this JSON with ALL sections filled:
{{"summary":"complete summary","bugs":["bug1","bug2"],"security_issues":["sec1","sec2"],"performance_issues":["perf1","perf2"],"suggestions":["fix1","fix2","fix3"],"improved_code":"completely production-ready code fixing ALL issues","score":3}}"""