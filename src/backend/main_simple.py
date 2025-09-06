"""
Luminis.AI Library Assistant - Simple Version
============================================

Simple version without complex dependencies for testing
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Luminis.AI Library Assistant API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "tr"


class ChatResponse(BaseModel):
    success: bool
    response: str
    user_message: str


# Sample book database
BOOKS_DATABASE = [
    {
        "title": "Suç ve Ceza",
        "author": "Fyodor Dostoyevski",
        "genre": "Roman",
        "description": "Psikolojik gerilim ve ahlaki sorgulama",
        "rating": 4.8,
        "year": 1866,
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genre": "Distopya",
        "description": "Totaliter rejim eleştirisi",
        "rating": 4.7,
        "year": 1949,
    },
    {
        "title": "Küçük Prens",
        "author": "Antoine de Saint-Exupéry",
        "genre": "Çocuk Edebiyatı",
        "description": "Felsefi masal",
        "rating": 4.9,
        "year": 1943,
    },
]


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint"""
    try:
        # Simple response logic
        if "kitap" in request.message.lower() or "book" in request.message.lower():
            response = "Merhaba! Size kitap önerileri sunabilirim. Hangi tür kitapları seversiniz?"
        elif "merhaba" in request.message.lower() or "hello" in request.message.lower():
            response = "Merhaba! Luminis AI Kütüphane Asistanı'na hoş geldiniz. Size nasıl yardımcı olabilirim?"
        else:
            response = "Teşekkürler! Size daha iyi yardımcı olabilmem için kitap tercihleriniz hakkında bilgi verebilir misiniz?"

        return ChatResponse(
            success=True, response=response, user_message=request.message
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books")
async def get_books():
    """Get all available books"""
    try:
        return {"success": True, "books": BOOKS_DATABASE, "count": len(BOOKS_DATABASE)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Luminis.AI Library Assistant API is running",
        "version": "1.0.0",
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Luminis.AI Library Assistant API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
