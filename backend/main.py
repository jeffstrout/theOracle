from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from app.api import astro, personality, auth

load_dotenv()

app = FastAPI(
    title="The Oracle API",
    description="Personality evaluation API using astrological data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(astro.router, prefix="/api/astro", tags=["astrology"])
app.include_router(personality.router, prefix="/api/personality", tags=["personality"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Welcome to The Oracle - Personality Evaluation API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oracle-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)