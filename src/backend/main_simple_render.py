"""
Simple FastAPI app for Render deployment
Minimal dependencies, maximum compatibility - no pydantic
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(
    title="Luminis AI Library Assistant",
    description="AI-powered library assistant",
    version="1.0.2",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Luminis AI Library Assistant API",
        "version": "1.0.2",
        "status": "running",
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "service": "luminis-backend", "version": "1.0.2"}


@app.get("/api/books")
async def get_books():
    """Get sample books"""
    return {
        "books": [
            {
                "id": 1,
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "genre": "Fiction",
                "description": "A classic American novel",
                "rating": 4.5,
                "year": 1925,
            },
            {
                "id": 2,
                "title": "1984",
                "author": "George Orwell",
                "genre": "Dystopian Fiction",
                "description": "A dystopian social science fiction novel",
                "rating": 4.7,
                "year": 1949,
            },
        ],
        "success": True,
    }


@app.post("/api/chat")
async def chat(message: dict):
    """Simple chat endpoint"""
    user_message = message.get("message", "")

    # Simple response without OpenAI for now
    response = f"Echo: {user_message}"

    return {
        "user_message": user_message,
        "response": response,
        "status": "success",
        "success": True,
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
