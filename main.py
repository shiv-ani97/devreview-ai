import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from schemas import CodeReviewRequest, CodeReviewResponse
from reviewer import review_code

app = FastAPI(
    title="DevReview AI",
    description="AI-Powered Code Review Tool for Developers",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/review", response_model=CodeReviewResponse)
async def review(request: CodeReviewRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    if len(request.code) > 10000:
        raise HTTPException(status_code=400, detail="Code too long. Max 10000 characters")
    
    result = await review_code(
        code=request.code,
        language=request.language,
        focus=request.focus
    )
    return result

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "DevReview AI"}