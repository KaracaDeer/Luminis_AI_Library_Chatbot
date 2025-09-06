"""
Minimal Backend for Testing - No Complex Dependencies

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import httpx
import asyncio
import random

app = FastAPI(title="Luminis.AI Library Assistant API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "tr"


class ChatResponse(BaseModel):
    success: bool
    response: str
    user_message: str
    books: Optional[List[dict]] = None


# Mock responses
MOCK_RESPONSES = {
    "tr": [
        "Merhaba! Ben Luminis.AI Kütüphane Asistanı. Size nasıl yardımcı olabilirim?",
        "Kitap dünyasında size rehberlik etmekten mutluluk duyarım! Hangi konuda yardıma ihtiyacınız var?",
        "Harika bir kitap arayışındasınız! Size en uygun önerileri bulabilirim.",
        "Edebiyat dünyasının kapılarını sizin için açalım! Ne tür kitaplar okumayı seviyorsunuz?",
    ],
    "en": [
        "Hello! I'm Luminis.AI Library Assistant. How can I help you?",
        "I'm happy to guide you in the world of books! What kind of help do you need?",
        "Great to see you're looking for books! I can find the best recommendations for you.",
        "Let's open the doors to the world of literature! What kind of books do you like to read?",
    ],
}

# Book categories and subjects for varied recommendations
BOOK_SUBJECTS = {
    "roman": ["fiction", "literature", "novel", "classic", "contemporary"],
    "bilim kurgu": ["science_fiction", "sci-fi", "dystopia", "space", "future"],
    "fantastik": ["fantasy", "magic", "adventure", "mythology", "epic"],
    "polisiye": ["mystery", "crime", "detective", "thriller", "suspense"],
    "tarih": ["history", "historical", "biography", "war", "ancient"],
    "felsefe": ["philosophy", "ethics", "metaphysics", "logic", "wisdom"],
    "psikoloji": ["psychology", "self-help", "mental_health", "behavior"],
    "edebiyat": ["literature", "poetry", "drama", "classics", "world_literature"],
    "klasik": ["classics", "ancient", "greek", "roman", "traditional"],
    "çocuk": ["children", "kids", "young_adult", "picture_book", "juvenile"],
}

# Turkish book database for Turkish language requests
TURKISH_BOOKS = {
    "roman": [
        {
            "title": "Aşk-ı Memnu",
            "author": "Halit Ziya Uşaklıgil",
            "genre": "Klasik Roman",
            "description": "Türk edebiyatının en önemli aşk romanı",
            "rating": 4.6,
            "year": 1900,
        },
        {
            "title": "Çalıkuşu",
            "author": "Reşat Nuri Güntekin",
            "genre": "Roman",
            "description": "Feride'nin hayat hikayesi",
            "rating": 4.7,
            "year": 1922,
        },
        {
            "title": "Kürk Mantolu Madonna",
            "author": "Sabahattin Ali",
            "genre": "Roman",
            "description": "Aşk ve özlem dolu bir hikaye",
            "rating": 4.8,
            "year": 1943,
        },
        {
            "title": "Tutunamayanlar",
            "author": "Oğuz Atay",
            "genre": "Modern Roman",
            "description": "Türk edebiyatının başyapıtı",
            "rating": 4.5,
            "year": 1971,
        },
        {
            "title": "Beyaz Gemi",
            "author": "Cengiz Aytmatov",
            "genre": "Roman",
            "description": "Doğa ve insanlık üzerine",
            "rating": 4.6,
            "year": 1970,
        },
    ],
    "bilim_kurgu": [
        {
            "title": "Gece Yarısı Kütüphanesi",
            "author": "Matt Haig",
            "genre": "Fantastik/Bilim Kurgu",
            "description": "Sonsuz yaşam olasılıkları",
            "rating": 4.4,
            "year": 2020,
        },
        {
            "title": "Dünyanın Sonundaki Kasaba",
            "author": "Murakami Haruki",
            "genre": "Bilim Kurgu",
            "description": "Gerçeklik ve hayal arasında",
            "rating": 4.3,
            "year": 1985,
        },
        {
            "title": "Zamanın Kırışıkları",
            "author": "Madeleine L'Engle",
            "genre": "Bilim Kurgu",
            "description": "Zaman yolculuğu macerası",
            "rating": 4.2,
            "year": 1962,
        },
    ],
    "polisiye": [
        {
            "title": "Kar",
            "author": "Orhan Pamuk",
            "genre": "Polisiye/Edebiyat",
            "description": "Kars'ta geçen gizemli bir hikaye",
            "rating": 4.1,
            "year": 2002,
        },
        {
            "title": "Şu Çılgın Türkler",
            "author": "Turgut Özakman",
            "genre": "Tarihsel Polisiye",
            "description": "Milli Mücadele dönemi",
            "rating": 4.5,
            "year": 1997,
        },
        {
            "title": "Madonna in a Fur Coat",
            "author": "Sabahattin Ali",
            "genre": "Klasik",
            "description": "Türk edebiyatının şaheseri",
            "rating": 4.8,
            "year": 1943,
        },
    ],
    "tarih": [
        {
            "title": "Nutuk",
            "author": "Mustafa Kemal Atatürk",
            "genre": "Tarih",
            "description": "Milli Mücadele'nin hikayesi",
            "rating": 4.9,
            "year": 1927,
        },
        {
            "title": "Devlet Ana",
            "author": "Kemal Tahir",
            "genre": "Tarihsel Roman",
            "description": "Osmanlı'dan Cumhuriyet'e geçiş",
            "rating": 4.4,
            "year": 1967,
        },
        {
            "title": "İstanbul: Hatıralar ve Şehir",
            "author": "Orhan Pamuk",
            "genre": "Anı/Tarih",
            "description": "İstanbul'un ruhunu anlatan eser",
            "rating": 4.3,
            "year": 2003,
        },
    ],
    "edebiyat": [
        {
            "title": "İnce Memed",
            "author": "Yaşar Kemal",
            "genre": "Edebiyat",
            "description": "Anadolu'nun epik hikayesi",
            "rating": 4.7,
            "year": 1955,
        },
        {
            "title": "Sefiller",
            "author": "Victor Hugo",
            "genre": "Klasik Edebiyat",
            "description": "İnsanlık ve adalet üzerine",
            "rating": 4.8,
            "year": 1862,
        },
        {
            "title": "Sinekli Bakkal",
            "author": "Halide Edib Adıvar",
            "genre": "Roman",
            "description": "Milli Mücadele dönemi",
            "rating": 4.5,
            "year": 1936,
        },
    ],
    "felsefe": [
        {
            "title": "Simyacı",
            "author": "Paulo Coelho",
            "genre": "Felsefi Roman",
            "description": "Kişisel efsaneyi bulma yolculuğu",
            "rating": 4.6,
            "year": 1988,
        },
        {
            "title": "Böyle Buyurdu Zerdüşt",
            "author": "Friedrich Nietzsche",
            "genre": "Felsefe",
            "description": "Nietzsche'nin felsefi şaheseri",
            "rating": 4.4,
            "year": 1883,
        },
        {
            "title": "Hayvan Çiftliği",
            "author": "George Orwell",
            "genre": "Alegorik Roman",
            "description": "Totalitarizm eleştirisi",
            "rating": 4.5,
            "year": 1945,
        },
    ],
}


async def search_books_openlibrary(
    query: str, subject: str = None, limit: int = 10
) -> List[Dict]:
    """Search books using Open Library API"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Build search parameters
            params = {
                "q": query,
                "limit": limit,
                "fields": "key,title,author_name,first_publish_year,subject,ratings_average,cover_i",
            }

            if subject:
                params["subject"] = subject

            print(
                f"DEBUG: Searching Open Library with query: {query}, subject: {subject}"
            )

            response = await client.get(
                "https://openlibrary.org/search.json", params=params
            )

            if response.status_code == 200:
                data = response.json()
                books = []

                for doc in data.get("docs", [])[:limit]:
                    book = {
                        "title": doc.get("title", "Bilinmeyen Kitap"),
                        "author": ", ".join(
                            doc.get("author_name", ["Bilinmeyen Yazar"])[:2]
                        ),
                        "genre": ", ".join(doc.get("subject", ["Genel"])[:2])
                        if doc.get("subject")
                        else "Genel",
                        "year": doc.get("first_publish_year", ""),
                        "rating": round(
                            doc.get("ratings_average", 0) or random.uniform(4.0, 4.8), 1
                        ),
                        "description": f"{doc.get('title', '')} - {', '.join(doc.get('author_name', [''])[:1])}",
                    }
                    books.append(book)

                print(f"DEBUG: Found {len(books)} books from Open Library")
                return books
            else:
                print(f"DEBUG: Open Library API error: {response.status_code}")
                return []

    except Exception as e:
        print(f"DEBUG: Error calling Open Library API: {e}")
        return []


def get_turkish_books_by_category(category: str, limit: int = 3) -> List[Dict]:
    """Get Turkish books from local database by category"""
    category_key = category.replace(" ", "_").lower()

    if category_key in TURKISH_BOOKS:
        books = TURKISH_BOOKS[category_key].copy()
        random.shuffle(books)
        return books[:limit]

    # If specific category not found, mix from all categories
    all_books = []
    for books_list in TURKISH_BOOKS.values():
        all_books.extend(books_list)

    random.shuffle(all_books)
    return all_books[:limit]


async def get_book_recommendations(
    user_message: str, language: str = "tr"
) -> List[Dict]:
    """Get book recommendations based on user message and language"""

    # Detect book category from message
    message_lower = user_message.lower()
    detected_category = None

    for category in BOOK_SUBJECTS.keys():
        if category in message_lower:
            detected_category = category
            break

    print(f"DEBUG: Detected category: {detected_category}, Language: {language}")

    # For Turkish language, prioritize Turkish books
    if language == "tr":
        turkish_books = []

        if detected_category:
            # Get Turkish books for specific category
            turkish_books = get_turkish_books_by_category(detected_category, limit=4)
            print(
                f"DEBUG: Found {len(turkish_books)} Turkish books for category: {detected_category}"
            )
        else:
            # Get mixed Turkish books
            turkish_books = get_turkish_books_by_category("roman", limit=2)
            turkish_books.extend(get_turkish_books_by_category("edebiyat", limit=2))
            print(f"DEBUG: Found {len(turkish_books)} mixed Turkish books")

        # Add one international book from Open Library for variety
        try:
            if detected_category and detected_category in BOOK_SUBJECTS:
                subjects = BOOK_SUBJECTS[detected_category]
                subject = random.choice(subjects)
                international_books = await search_books_openlibrary(
                    "", subject=subject, limit=1
                )
                if international_books:
                    turkish_books.extend(international_books[:1])
                    print(f"DEBUG: Added 1 international book")
        except Exception as e:
            print(f"DEBUG: Error getting international book: {e}")

        random.shuffle(turkish_books)
        return turkish_books[:5]

    else:
        # For English language, use Open Library API
        detected_subjects = []

        if detected_category and detected_category in BOOK_SUBJECTS:
            detected_subjects.extend(BOOK_SUBJECTS[detected_category])

        # Default subjects if no specific category detected
        if not detected_subjects:
            detected_subjects = ["fiction", "literature", "bestseller"]

        # Try different search approaches
        all_books = []

        # 1. Search with detected subject
        if detected_subjects:
            subject = random.choice(detected_subjects)
            books = await search_books_openlibrary("", subject=subject, limit=5)
            all_books.extend(books)

        # 2. Search popular/classic books
        popular_queries = ["bestseller", "popular", "award winning", "classic"]
        for query in popular_queries[:2]:
            books = await search_books_openlibrary(query, limit=3)
            all_books.extend(books)

        # Remove duplicates and shuffle
        seen_titles = set()
        unique_books = []
        for book in all_books:
            title_key = book["title"].lower().strip()
            if title_key not in seen_titles and len(title_key) > 2:
                seen_titles.add(title_key)
                unique_books.append(book)

        # Shuffle and return max 5 books
        random.shuffle(unique_books)
        return unique_books[:5]


# Endpoints
@app.get("/")
async def root():
    return {
        "message": "Luminis.AI Library Assistant API",
        "version": "1.0.0",
        "status": "running",
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for AI library assistant"""
    try:
        user_message = request.message
        user_language = request.language or "tr"

        print(f"DEBUG: Received chat message: {user_message}")
        print(f"DEBUG: Language: {user_language}")

        # Check if the message is asking for book recommendations
        book_keywords = [
            "kitap öner",
            "book recommend",
            "öner",
            "recommend",
            "kitap",
            "book",
            "roman",
            "novel",
            "edebiyat",
            "literature",
            "bilim kurgu",
            "fantastik",
            "klasik",
            "polisiye",
            "tarih",
            "felsefe",
            "psikoloji",
        ]
        is_book_request = any(
            keyword in user_message.lower() for keyword in book_keywords
        )
        print(f"DEBUG: Book request detected: {is_book_request}")

        # Simple mock response
        import random

        responses = MOCK_RESPONSES.get(user_language, MOCK_RESPONSES["tr"])
        ai_response = random.choice(responses)

        # If it's a book recommendation request, get dynamic recommendations
        books_data = None
        if is_book_request:
            print("DEBUG: Getting dynamic book recommendations from Open Library")
            books_data = await get_book_recommendations(user_message, user_language)

            # Fallback to static books if API fails
            if not books_data:
                print("DEBUG: Falling back to static book recommendations")
                books_data = [
                    {
                        "title": "Suç ve Ceza",
                        "author": "Fyodor Dostoyevski",
                        "genre": "Klasik Roman",
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
                        "title": "Hobbit",
                        "author": "J.R.R. Tolkien",
                        "genre": "Fantastik",
                        "description": "Macera dolu fantastik roman",
                        "rating": 4.8,
                        "year": 1937,
                    },
                ]

        return ChatResponse(
            success=True,
            response=ai_response,
            user_message=user_message,
            books=books_data,
        )

    except Exception as e:
        print(f"ERROR in chat endpoint: {e}")
        return ChatResponse(
            success=False,
            response=f"Üzgünüm, bir hata oluştu: {str(e)}",
            user_message=request.message,
            books=None,
        )


@app.get("/api/books")
async def get_books():
    """Get all books"""
    try:
        # Mock books data
        books = [
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
        ]

        return {"success": True, "books": books}

    except Exception as e:
        print(f"ERROR in books endpoint: {e}")
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn

    print("Starting Luminis.AI Backend on port 5000...")
    uvicorn.run(app, host="0.0.0.0", port=5000)
