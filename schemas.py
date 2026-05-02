from pydantic import BaseModel

class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    focus: str = "general"  # general, security, performance, bugs

class CodeReviewResponse(BaseModel):
    summary: str
    bugs: list[str]
    security_issues: list[str]
    performance_issues: list[str]
    suggestions: list[str]
    improved_code: str
    score: int  # 1-10