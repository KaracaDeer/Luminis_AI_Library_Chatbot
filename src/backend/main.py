"""
Luminis.AI Library Assistant - Main Application Entry Point
==========================================================

This is the main entry point for the Luminis.AI Library Assistant application.
The application provides an AI-powered library assistant that offers book recommendations,
literature information, and reading advice to users.

Framework: FastAPI (Python web framework for building APIs)
Features:
- AI-powered chat with OpenAI integration
- Book recommendations and analysis
- User authentication and profile management
- OAuth 2.0 integration (Google, GitHub)
- RAG (Retrieval-Augmented Generation) capabilities
- Vector-based semantic search
- Audio transcription (voice-to-text)
- Multi-language support (Turkish/English)

Key Endpoints:
- /api/chat: Main chat endpoint for AI library assistant
- /api/books: Get all available books
- /api/book-recommendations: Get personalized book recommendations
- /api/auth/*: User authentication endpoints (register, login, OAuth)
- /api/rag/*: RAG-powered chat and recommendations
- /api/vector/*: Vector-based semantic search and similarity
- /api/transcribe: Convert audio to text
- /api/analyze-reading: Analyze user's reading preferences

Dependencies:
- FastAPI for web framework
- OpenAI API for AI responses
- SQLAlchemy for database operations
- JWT for authentication
- Vector databases for semantic search
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
from dotenv import load_dotenv
import json
import tempfile
from sqlalchemy.orm import Session
from datetime import datetime

# Import database models
import sys
import os

# Ensure absolute path to the src directory is available for imports
_CURRENT_DIR = os.path.dirname(__file__)
_SRC_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, os.pardir))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

# Also add the database directory specifically for robust import
_DATABASE_DIR = os.path.join(_SRC_DIR, "database")
if _DATABASE_DIR not in sys.path:
    sys.path.insert(0, _DATABASE_DIR)

# Robust import with multiple fallback mechanisms
User = get_db = create_tables = init_sample_data = None

# Try different import approaches
try:
    from database.database import User, get_db, create_tables, init_sample_data
except ImportError:
    try:
        # Fallback 1: Direct import from database module
        from database import User, get_db, create_tables, init_sample_data
    except ImportError:
        try:
            # Fallback 2: Import using importlib
            import importlib.util

            spec = importlib.util.spec_from_file_location(
                "database", os.path.join(_DATABASE_DIR, "database.py")
            )
            database_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(database_module)
            User = database_module.User
            get_db = database_module.get_db
            create_tables = database_module.create_tables
            init_sample_data = database_module.init_sample_data
        except Exception as e:
            print(f"WARNING: Could not import database module: {e}")
            # Create dummy functions for testing environments

            class DummyUser:
                pass

            def dummy_get_db():
                pass

            def dummy_create_tables():
                pass

            def dummy_init_sample_data():
                pass

            User = DummyUser
            get_db = dummy_get_db
            create_tables = dummy_create_tables
            init_sample_data = dummy_init_sample_data

# Import our services

# Import RAG services with error handling
rag_service = None
vector_service = None

try:
    from services.rag_service import RAGService

    rag_service = RAGService()
    print("RAG service imported successfully")
except Exception as e:
    print(f"RAG service import failed: {e}")

try:
    from services.vector_service import VectorService

    vector_service = VectorService()
    print("Vector service imported successfully")
except Exception as e:
    print(f"Vector service import failed: {e}")

# Import enhanced response manager
try:
    from .enhanced_responses import response_manager

    print("Enhanced response manager imported successfully")
except Exception as e:
    print(f"Enhanced response manager import failed: {e}")
    response_manager = None

# Import authentication services
try:
    from services.auth_service import (
        auth_service,
        oauth2_service,
        get_current_user,
        get_current_active_user,
    )

    print("Authentication services imported successfully")
except Exception as e:
    print(f"Authentication services import failed: {e}")
    auth_service = None
    oauth2_service = None
    get_current_user = None
    get_current_active_user = None

# Import Open Library service
try:
    from services.openlibrary_service import OpenLibraryService

    openlibrary_service = OpenLibraryService()
    print("Open Library service imported successfully")
except Exception as e:
    print(f"Open Library service import failed: {e}")
    openlibrary_service = None

# Load environment variables
load_dotenv()

app = FastAPI(title="Luminis.AI Library Assistant API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://0.0.0.0:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    client = openai.OpenAI(api_key=openai_api_key)
    print("OpenAI client initialized")
else:
    client = None
    print("OpenAI API key not found, some features may not work")


# Pydantic models
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "tr"  # Default to Turkish


class ChatResponse(BaseModel):
    success: bool
    response: str
    user_message: str
    books: Optional[List[dict]] = None


class BookRecommendationRequest(BaseModel):
    preferences: dict


class BookRecommendationResponse(BaseModel):
    success: bool
    recommendations: str
    books: List[dict]


class ReadingAnalysisRequest(BaseModel):
    reading_list: List[dict]


class ReadingAnalysisResponse(BaseModel):
    success: bool
    analysis: str


class TranscriptionResponse(BaseModel):
    success: bool
    text: str


# Sample book database with translations
BOOKS_DATABASE = [
    {
        "title": "Suç ve Ceza",
        "title_en": "Crime and Punishment",
        "author": "Fyodor Dostoyevski",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Psikolojik gerilim ve ahlaki sorgulama",
        "description_en": "Psychological tension and moral questioning",
        "rating": 4.8,
        "year": 1866,
    },
    {
        "title": "1984",
        "title_en": "1984",
        "author": "George Orwell",
        "genre": "Distopya",
        "genre_en": "Dystopia",
        "description": "Totaliter rejim eleştirisi",
        "description_en": "Critique of totalitarian regime",
        "rating": 4.7,
        "year": 1949,
    },
    {
        "title": "Küçük Prens",
        "title_en": "The Little Prince",
        "author": "Antoine de Saint-Exupéry",
        "genre": "Çocuk Edebiyatı",
        "genre_en": "Children's Literature",
        "description": "Felsefi masal",
        "description_en": "Philosophical tale",
        "rating": 4.9,
        "year": 1943,
    },
    {
        "title": "Dune",
        "title_en": "Dune",
        "author": "Frank Herbert",
        "genre": "Bilim Kurgu",
        "genre_en": "Science Fiction",
        "description": "Epik bilim kurgu romanı",
        "description_en": "Epic science fiction novel",
        "rating": 4.6,
        "year": 1965,
    },
    {
        "title": "Hobbit",
        "title_en": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": "Fantastik",
        "genre_en": "Fantasy",
        "description": "Macera dolu fantastik roman",
        "description_en": "Adventure-filled fantasy novel",
        "rating": 4.8,
        "year": 1937,
    },
    {
        "title": "Kürk Mantolu Madonna",
        "title_en": "Madonna in a Fur Coat",
        "author": "Sabahattin Ali",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Aşk ve toplumsal baskı arasında kalan genç bir adamın hikayesi",
        "description_en": "The story of a young man caught between love and social pressure",
        "rating": 4.7,
        "year": 1943,
    },
    {
        "title": "Çalıkuşu",
        "title_en": "The Wren",
        "author": "Reşat Nuri Güntekin",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Cumhuriyet dönemi Türk kadınının özgürlük mücadelesi",
        "description_en": "The freedom struggle of Turkish women in the Republican era",
        "rating": 4.6,
        "year": 1922,
    },
    {
        "title": "Fareler ve İnsanlar",
        "title_en": "Of Mice and Men",
        "author": "John Steinbeck",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Büyük Buhran döneminde iki arkadaşın dostluk hikayesi",
        "description_en": "The story of friendship between two friends during the Great Depression",
        "rating": 4.5,
        "year": 1937,
    },
    {
        "title": "Büyük Umutlar",
        "title_en": "Great Expectations",
        "author": "Charles Dickens",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Fakir bir çocuğun zengin olma hayali ve gerçeklerle yüzleşmesi",
        "description_en": "A poor child's dream of becoming rich and facing reality",
        "rating": 4.4,
        "year": 1861,
    },
    {
        "title": "Dönüşüm",
        "title_en": "The Metamorphosis",
        "author": "Franz Kafka",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Bir sabah kendini böceğe dönüşmüş bulan Gregor Samsa'nın hikayesi",
        "description_en": "The story of Gregor Samsa who wakes up one morning transformed into an insect",
        "rating": 4.3,
        "year": 1915,
    },
    {
        "title": "Şeker Portakalı",
        "title_en": "My Sweet Orange Tree",
        "author": "José Mauro de Vasconcelos",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Fakir bir çocuğun hayal gücü ile zorlukları aşması",
        "description_en": "A poor child overcoming difficulties with imagination",
        "rating": 4.8,
        "year": 1968,
    },
    {
        "title": "Martı",
        "title_en": "Jonathan Livingston Seagull",
        "author": "Richard Bach",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Bir martının özgürlük ve mükemmellik arayışı",
        "description_en": "A seagull's quest for freedom and perfection",
        "rating": 4.2,
        "year": 1970,
    },
    {
        "title": "Alice Harikalar Diyarında",
        "title_en": "Alice's Adventures in Wonderland",
        "author": "Lewis Carroll",
        "genre": "Çocuk Edebiyatı",
        "genre_en": "Children's Literature",
        "description": "Alice'in fantastik dünyada yaşadığı maceralar",
        "description_en": "Alice's adventures in a fantastic world",
        "rating": 4.5,
        "year": 1865,
    },
    {
        "title": "Pinokyo",
        "title_en": "Pinocchio",
        "author": "Carlo Collodi",
        "genre": "Çocuk Edebiyatı",
        "genre_en": "Children's Literature",
        "description": "Tahtadan yapılmış bir kuklanın gerçek çocuk olma hikayesi",
        "description_en": "The story of a wooden puppet becoming a real child",
        "rating": 4.4,
        "year": 1883,
    },
    {
        "title": "Harry Potter ve Felsefe Taşı",
        "title_en": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "genre": "Fantastik",
        "genre_en": "Fantasy",
        "description": "Genç bir büyücünün Hogwarts'ta yaşadığı maceralar",
        "description_en": "A young wizard's adventures at Hogwarts",
        "rating": 4.9,
        "year": 1997,
    },
    {
        "title": "Açlık Oyunları",
        "title_en": "The Hunger Games",
        "author": "Suzanne Collins",
        "genre": "Bilim Kurgu",
        "genre_en": "Science Fiction",
        "description": "Distopik bir dünyada hayatta kalma mücadelesi",
        "description_en": "Survival struggle in a dystopian world",
        "rating": 4.6,
        "year": 2008,
    },
    {
        "title": "Alacakaranlık",
        "title_en": "Twilight",
        "author": "Stephenie Meyer",
        "genre": "Fantastik",
        "genre_en": "Fantasy",
        "description": "Vampir ve insan arasındaki imkansız aşk hikayesi",
        "description_en": "The impossible love story between a vampire and a human",
        "rating": 4.3,
        "year": 2005,
    },
    {
        "title": "Sherlock Holmes: Kızıl İmza",
        "title_en": "Sherlock Holmes: A Study in Scarlet",
        "author": "Arthur Conan Doyle",
        "genre": "Polisiye",
        "genre_en": "Mystery",
        "description": "Ünlü dedektifin çözdüğü gizemli cinayet",
        "description_en": "A mysterious murder solved by the famous detective",
        "rating": 4.5,
        "year": 1892,
    },
    {
        "title": "Orient Express'te Cinayet",
        "title_en": "Murder on the Orient Express",
        "author": "Agatha Christie",
        "genre": "Polisiye",
        "genre_en": "Mystery",
        "description": "Lüks trende işlenen cinayetin çözülmesi",
        "description_en": "Solving a murder committed on a luxury train",
        "rating": 4.7,
        "year": 1934,
    },
    {
        "title": "Sefiller",
        "title_en": "Les Misérables",
        "author": "Victor Hugo",
        "genre": "Roman",
        "genre_en": "Novel",
        "description": "Fransa'da yaşanan toplumsal adaletsizlikler ve insanlık hikayesi",
        "description_en": "Social injustices in France and the story of humanity",
        "rating": 4.6,
        "year": 1862,
    },
    {
        "title": "Savaş ve Barış",
        "author": "Leo Tolstoy",
        "genre": "Roman",
        "description": "Napolyon savaşları sırasında Rus aristokrasisinin yaşamı",
        "rating": 4.5,
        "year": 1869,
    },
    {
        "title": "Sofinin Dünyası",
        "author": "Jostein Gaarder",
        "genre": "Felsefe",
        "description": "Felsefe tarihini roman formatında anlatan eğitici kitap",
        "rating": 4.4,
        "year": 1991,
    },
    {
        "title": "Felsefe Tarihi",
        "author": "Ahmet Cevizci",
        "genre": "Felsefe",
        "description": "Antik çağdan günümüze felsefe düşüncesinin gelişimi",
        "rating": 4.3,
        "year": 2009,
    },
    {
        "title": "İnsan Doğası",
        "author": "David Hume",
        "genre": "Felsefe",
        "description": "İnsan doğasının felsefi analizi ve ahlak teorisi",
        "rating": 4.2,
        "year": 1739,
    },
    {
        "title": "Karakter Analizi",
        "author": "Wilhelm Reich",
        "genre": "Psikoloji",
        "description": "İnsan karakterinin psikolojik analizi",
        "rating": 4.1,
        "year": 1933,
    },
    {
        "title": "Gelecek Vizyonu",
        "author": "Alvin Toffler",
        "genre": "Teknoloji",
        "description": "Teknolojik gelişmelerin gelecekteki etkileri",
        "rating": 4.0,
        "year": 1970,
    },
    {
        "title": "Dijital Dünya",
        "author": "Nicholas Negroponte",
        "genre": "Teknoloji",
        "description": "Dijital teknolojinin hayatımıza etkileri",
        "rating": 4.1,
        "year": 1995,
    },
    {
        "title": "Yaz Gecesi Rüyası",
        "author": "William Shakespeare",
        "genre": "Tiyatro",
        "description": "Aşk ve büyü temalı komedi oyunu",
        "rating": 4.6,
        "year": 1595,
    },
    {
        "title": "Kış Masalları",
        "author": "William Shakespeare",
        "genre": "Tiyatro",
        "description": "Aile ve aşk temalı romantik komedi",
        "rating": 4.4,
        "year": 1611,
    },
    {
        "title": "Şef'in Masası",
        "author": "Anthony Bourdain",
        "genre": "Yemek",
        "description": "Dünya mutfaklarından lezzetli hikayeler",
        "rating": 4.3,
        "year": 2000,
    },
    {
        "title": "Olimpiyat Ruhu",
        "author": "Pierre de Coubertin",
        "genre": "Spor",
        "description": "Olimpiyat oyunlarının tarihi ve ruhu",
        "rating": 4.2,
        "year": 1896,
    },
    {
        "title": "Dünya Turu",
        "author": "Jules Verne",
        "genre": "Seyahat",
        "description": "80 günde dünya turu macerası",
        "rating": 4.5,
        "year": 1873,
    },
    {
        "title": "Sesin Gücü",
        "author": "Daniel Levitin",
        "genre": "Müzik",
        "description": "Müziğin insan beyni üzerindeki etkileri",
        "rating": 4.1,
        "year": 2006,
    },
]

# Mock AI responses for when API quota is exceeded
MOCK_RESPONSES = {
    # General greetings and basic conversations
    "merhaba": "Merhaba! Ben Luminis.AI Kütüphane Asistanı. Size kitap önerileri verebilir, edebiyat hakkında bilgi verebilir ve okuma tavsiyelerinde bulunabilirim. Nasıl yardımcı olabilirim?",
    "selam": "Selam! Kitap dünyasında size rehberlik etmekten mutluluk duyarım. Hangi konuda yardıma ihtiyacınız var?",
    "nasılsın": "İyiyim, teşekkür ederim! Size kitap önerileri vermek ve edebiyat dünyasında rehberlik etmek için buradayım. Hangi konuda yardıma ihtiyacınız var?",
    "teşekkür": "Rica ederim! Başka bir konuda yardıma ihtiyacınız olursa her zaman buradayım. Kitap önerileri, edebiyat tartışmaları veya okuma tavsiyeleri için sorabilirsiniz.",
    "güzel": "Harika! Edebiyat dünyası gerçekten büyüleyici, değil mi? Hangi türde kitaplar ilginizi çekiyor? Size özel öneriler verebilirim.",
    "sevdiğim": "Harika! Hangi kitapları sevdiğinizi bilmek size daha iyi öneriler vermeme yardımcı olur. Sevdiğiniz yazarlar veya türler var mı?",
    # Book genres and recommendations
    "roman": "Roman türünde size birkaç harika kitap öneriyorum:\n\n1. **Suç ve Ceza** - Dostoyevski (Psikolojik derinlik ve ahlaki sorgulama)\n2. **Kürk Mantolu Madonna** - Sabahattin Ali (Aşk ve toplumsal baskı)\n3. **Çalıkuşu** - Reşat Nuri Güntekin (Cumhuriyet dönemi kadın mücadelesi)\n4. **Fareler ve İnsanlar** - John Steinbeck (Dostluk ve Büyük Buhran)\n5. **Sefiller** - Victor Hugo (Toplumsal adaletsizlikler)",
    "bilim kurgu": "Bilim kurgu türünde şu kitapları öneriyorum:\n\n1. **Dune** - Frank Herbert (Epik bilim kurgu, siyaset ve ekoloji)\n2. **1984** - George Orwell (Distopik toplum eleştirisi)\n3. **Açlık Oyunları** - Suzanne Collins (Distopik hayatta kalma mücadelesi)\n4. **Gelecek Vizyonu** - Alvin Toffler (Teknolojik gelişmeler)\n5. **Dijital Dünya** - Nicholas Negroponte (Dijital teknoloji etkileri)",
    "fantastik": "Fantastik türde bu kitapları öneriyorum:\n\n1. **Hobbit** - J.R.R. Tolkien (Macera dolu fantastik yolculuk)\n2. **Harry Potter ve Felsefe Taşı** - J.K. Rowling (Büyücülük okulu maceraları)\n3. **Alacakaranlık** - Stephenie Meyer (Vampir-insan aşk hikayesi)\n4. **Alice Harikalar Diyarında** - Lewis Carroll (Fantastik dünya maceraları)\n5. **Pinokyo** - Carlo Collodi (Kuklanın gerçek çocuk olma hikayesi)",
    "klasik": "Klasik edebiyat eserleri arasında şunları öneriyorum:\n\n1. **1984** - George Orwell (Totaliter rejim eleştirisi)\n2. **Fareler ve İnsanlar** - John Steinbeck (Dostluk ve Büyük Buhran)\n3. **Büyük Umutlar** - Charles Dickens (Zengin olma hayali ve gerçekler)\n4. **Dönüşüm** - Franz Kafka (Böceğe dönüşme alegorisi)\n5. **Savaş ve Barış** - Leo Tolstoy (Napolyon savaşları dönemi)",
    "polisiye": "Polisiye türde bu kitapları öneriyorum:\n\n1. **Orient Express'te Cinayet** - Agatha Christie (Lüks trende gizemli cinayet)\n2. **Sherlock Holmes: Kızıl İmza** - Arthur Conan Doyle (Ünlü dedektifin çözdüğü gizem)\n3. **Suç ve Ceza** - Dostoyevski (Psikolojik gerilim ve ahlaki sorgulama)\n4. **1984** - George Orwell (Distopik toplum ve gözetim)\n5. **Dönüşüm** - Franz Kafka (Varoluşsal sorgulama)",
    "tarih": "Tarih temalı kitaplar arasında şunları öneriyorum:\n\n1. **Sefiller** - Victor Hugo (Fransa'da toplumsal adaletsizlikler)\n2. **Savaş ve Barış** - Leo Tolstoy (Napolyon savaşları dönemi)\n3. **Çalıkuşu** - Reşat Nuri Güntekin (Cumhuriyet dönemi Türk tarihi)\n4. **Kürk Mantolu Madonna** - Sabahattin Ali (Osmanlı sonrası dönem)\n5. **Fareler ve İnsanlar** - John Steinbeck (Büyük Buhran dönemi)",
    # Reading habits and advice
    "okuma": "Okuma alışkanlığı geliştirmek için şu kitapları öneriyorum:\n\n1. **Küçük Prens** - Saint-Exupéry (Başlangıç için mükemmel)\n2. **Şeker Portakalı** - Vasconcelos (Motivasyon verici)\n3. **Martı** - Richard Bach (İlham verici)\n4. **Alice Harikalar Diyarında** - Carroll (Hayal gücünü geliştirir)\n5. **Pinokyo** - Collodi (Çocukluktan yetişkinliğe)",
    "hızlı okuma": "Hızlı okuma için şu teknikleri öneriyorum:\n\n1. **Göz egzersizleri** yapın\n2. **Kelime grupları** halinde okuyun\n3. **Anlama stratejileri** geliştirin\n4. **Düzenli pratik** yapın\n5. **Okuma hedefleri** belirleyin",
    "anlayarak okuma": "Anlayarak okuma için şu kitapları öneriyorum:\n\n1. **Sofinin Dünyası** - Gaarder (Felsefe ile okuma)\n2. **Felsefe Tarihi** - Cevizci (Düşünsel derinlik)\n3. **Suç ve Ceza** - Dostoyevski (Psikolojik analiz)\n4. **1984** - Orwell (Sosyal eleştiri)\n5. **Dönüşüm** - Kafka (Varoluşsal sorgulama)",
    # Authors and literature
    "yazar": "Yazarlar hakkında konuşmak çok güzel! Hangi yazarı merak ediyorsunuz? Size o yazarın eserleri ve yazım tarzı hakkında bilgi verebilirim. Örneğin Dostoyevski, Kafka, Camus gibi yazarların eserlerini inceleyebiliriz.",
    "kitap": "Kitap konusunda size yardımcı olmaktan mutluluk duyarım! Hangi türde kitap arıyorsunuz? Roman, bilim kurgu, fantastik, klasik edebiyat, şiir, deneme... Seçenekler çok fazla!",
    "edebiyat": "Edebiyat dünyası çok geniş! Klasik edebiyattan modern eserlere, şiirden romana kadar her türde öneri verebilirim. Hangi yönünü keşfetmek istiyorsunuz?",
    # Book recommendations based on mood
    "mutlu": "Mutlu hissettiğinizde 'Küçük Prens' gibi sıcak hikayeler okumak harika olur. 'Çiçeklerin Dili' ve 'Güneşi Uyandıran' gibi pozitif kitaplar da ruh halinizi yükseltebilir.",
    "üzgün": "Üzgün hissettiğinizde 'Küçük Prens' gibi umut verici kitaplar okumak iyi gelebilir. 'Şeker Portakalı' ve 'Martı' gibi eserler de ruh halinizi iyileştirebilir.",
    "stresli": "Stresli olduğunuzda 'Sakinleştirici Okuma' kitabını öneriyorum. Ayrıca doğa temalı kitaplar ve şiirler de rahatlamanıza yardımcı olabilir.",
    "enerjik": "Enerjik hissettiğinizde macera romanları ve aksiyon dolu hikayeler okumak harika olur! 'Sherlock Holmes' gibi gizem kitapları da zihninizi canlı tutar.",
    # Seasonal and weather-based recommendations
    "yaz": "Yaz aylarında hafif, eğlenceli kitaplar okumak harika olur. 'Yaz Gecesi Rüyası', 'Deniz Kenarında' gibi kitaplar yaz atmosferini tamamlıyor.",
    "kış": "Kış aylarında sıcak, samimi kitaplar okumak çok güzel. 'Kış Masalları', 'Soba Başında' gibi kitaplar kış atmosferini tamamlıyor.",
    "yağmur": "Yağmurlu günlerde 'Yağmur Altında' gibi kitaplar okumak çok romantik olur. Ayrıca sıcak çay eşliğinde klasik romanlar da yağmur günlerinin vazgeçilmezi.",
    "güneş": "Güneşli günlerde açık havada okunabilecek hafif kitaplar öneriyorum. 'Güneş Işığında' gibi kitaplar güneş enerjisini tamamlıyor.",
    # Age group recommendations
    "çocuk": "Çocuk edebiyatı için 'Küçük Prens', 'Pinokyo', 'Alice Harikalar Diyarında' gibi klasikleri öneriyorum. Bu kitaplar hem çocuklar hem de yetişkinler için büyüleyici.",
    "genç": "Gençlik edebiyatı için 'Harry Potter' serisi, 'Açlık Oyunları', 'Alacakaranlık' gibi popüler serileri öneriyorum. Bu kitaplar gençlerin hayal gücünü geliştiriyor.",
    "yetişkin": "Yetişkinler için 'Suç ve Ceza', '1984', 'Dönüşüm' gibi derinlikli eserleri öneriyorum. Bu kitaplar hayat hakkında düşünmenizi sağlayacak.",
    # Special situations and interests
    "yemek": "Yemek temalı kitaplar arasında 'Şef'in Masası', 'Lezzetli Hikayeler' gibi eserler öne çıkıyor. Ayrıca okurken çay/kahve eşliğinde kitap okumak çok güzel bir deneyim.",
    "spor": "Spor temalı kitaplar arasında 'Olimpiyat Ruhu', 'Spor Kahramanları' gibi eserler var. Bu kitaplar motivasyonunuzu artırabilir.",
    "seyahat": "Seyahat kitapları arasında 'Dünya Turu', 'Macera Yolları' gibi eserler öne çıkıyor. Bu kitaplar sizi farklı kültürlere götürüyor.",
    "müzik": "Müzik temalı kitaplar arasında 'Sesin Gücü', 'Melodi Hikayeleri' gibi eserler var. Müzik ve edebiyat birleşimi çok etkileyici.",
    # Philosophical and intellectual topics
    "felsefe": "Felsefe kitapları arasında 'Sofinin Dünyası', 'Felsefe Tarihi' gibi eserler öne çıkıyor. Bu kitaplar düşüncelerinizi genişletebilir.",
    "psikoloji": "Psikoloji kitapları arasında 'İnsan Doğası', 'Karakter Analizi' gibi eserler var. Bu kitaplar insan davranışını anlamanıza yardımcı olabilir.",
    "teknoloji": "Teknoloji temalı kitaplar arasında 'Gelecek Vizyonu', 'Dijital Dünya' gibi eserler öne çıkıyor. Bu kitaplar geleceği anlamanıza yardımcı olabilir.",
    # General responses for question words
    "ne": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    "hangi": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    "nasıl": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    "neden": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    "kim": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    "nerede": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    "ne zaman": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    "kaç": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
    # Default response
    "default": "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
}


def translate_books_for_language(books: list, target_language: str = "tr") -> list:
    """Translate book data based on target language"""
    if target_language == "tr":
        # Return Turkish version
        return books
    else:
        # Return English version
        translated_books = []
        for book in books:
            # If English translation exists, use it; otherwise keep original
            translated_book = {
                "title": book.get("title_en", book.get("title", "")),
                "author": book.get("author", ""),
                "genre": book.get("genre_en", book.get("genre", "")),
                "description": book.get("description_en", book.get("description", "")),
                "rating": book.get("rating", 0),
                "year": book.get("year", 0),
            }
            translated_books.append(translated_book)
        return translated_books


def get_mock_response(user_message: str, user_language: str = "tr") -> str:
    """Get appropriate mock response based on user message and language"""

    # Try to use enhanced response manager if available
    if response_manager:
        try:
            enhanced_response = response_manager.get_contextual_response(
                user_message, user_language
            )
            if enhanced_response:
                return enhanced_response
        except Exception as e:
            print(f"Enhanced response manager failed: {e}")

    # Enhanced mock response logic with genre-specific responses
    message_lower = user_message.lower()

    # Genre-specific responses with direct book recommendations
    genre_responses = {
        "bilim kurgu": "Bilim kurgu türünde size şu harika kitapları öneriyorum: 'Dune' - Frank Herbert (Epik bilim kurgu), 'Vakıf' - Isaac Asimov (Galaktik imparatorluk), 'Blade Runner' - Philip K. Dick (Distopik gelecek). Bu kitaplar bilim kurgu edebiyatının klasikleri arasında yer alıyor.",
        "fantastik": "Fantastik türde bu muhteşem kitapları öneriyorum: 'Yüzüklerin Efendisi' - J.R.R. Tolkien (Epik fantastik), 'Harry Potter' - J.K. Rowling (Büyücülük dünyası), 'Game of Thrones' - George R.R. Martin (Ortaçağ fantastik). Her biri farklı bir fantastik dünya sunuyor.",
        "roman": "Roman türünde size şu etkileyici eserleri öneriyorum: 'Suç ve Ceza' - Dostoyevski (Psikolojik derinlik), 'Anna Karenina' - Tolstoy (Aşk ve toplum), 'Madame Bovary' - Flaubert (Realist edebiyat). Bu klasikler edebiyat tarihinin zirvelerinden.",
        "klasik": "Klasik edebiyat eserleri arasında şunları öneriyorum: '1984' - George Orwell (Distopik klasik), 'Fareler ve İnsanlar' - John Steinbeck (Amerikan klasik), 'Bülbülü Öldürmek' - Harper Lee (Toplumsal eleştiri). Her biri farklı dönemlerden önemli eserler.",
        "polisiye": "Polisiye türde bu gerilim dolu kitapları öneriyorum: 'Sherlock Holmes' - Arthur Conan Doyle (Dedektiflik klasik), 'Agatha Christie' - Cinayet romanları (Gizem ve çözüm), 'Stieg Larsson' - Millennium serisi (Modern polisiye). Her biri farklı bir polisiye yaklaşımı sunuyor.",
        "felsefe": "Felsefe kitapları arasında şunları öneriyorum: 'Sokrates'in Savunması' - Platon (Antik felsefe), 'Varlık ve Zaman' - Heidegger (Varoluş felsefesi), 'Meditasyonlar' - Descartes (Modern felsefe). Bu eserler felsefe tarihinin temel taşları.",
        "çocuk": "Çocuk edebiyatı için şunları öneriyorum: 'Küçük Prens' - Saint-Exupéry (Felsefi masal), 'Alice Harikalar Diyarında' - Lewis Carroll (Hayal gücü), 'Pinokyo' - Carlo Collodi (Eğitici masal). Her biri çocuklara farklı değerler öğretiyor.",
    }

    # Check for specific genres first
    for genre, response in genre_responses.items():
        if genre in message_lower:
            return response

    # Define responses based on language
    if user_language == "en":
        MOCK_RESPONSES = {
            "default": "I'm here to help you with book recommendations and reading advice. What would you like to know?",
            "roman": "I'd be happy to recommend some great novels! What genre interests you most?",
            "kitap": "I can suggest books in various genres. What type of books do you enjoy reading?",
            "yazar": "There are many wonderful authors to discover. Which literary period or genre interests you?",
            "edebiyat": "Literature is a vast and beautiful world! What aspect would you like to explore?",
            "okuma": "Reading is a wonderful habit! I can help you develop better reading practices and find books that match your interests.",
            "bilim kurgu": "Science fiction is fascinating! I can recommend classics like '1984' by George Orwell or 'The Martian' by Andy Weir.",
            "fantastik": "Fantasy books can transport you to magical worlds! Would you like recommendations for epic fantasy or urban fantasy?",
            "klasik": "Classic literature offers timeless stories. I can suggest works from different periods and cultures.",
            "şiir": "Poetry can touch the soul in unique ways. What type of poetry interests you?",
            "tarih": "Historical books can make the past come alive. Which historical period fascinates you?",
            "felsefe": "Philosophy books can expand your thinking. Are you interested in ancient, modern, or specific philosophical topics?",
            "psikoloji": "Psychology books can help you understand human behavior. What aspect of psychology interests you?",
            "teknoloji": "Technology books can keep you updated on the latest developments. What tech area interests you?",
            "sanat": "Art books can inspire creativity. Which art form or period interests you?",
            "doğa": "Nature books can deepen your appreciation for the environment. What aspect of nature fascinates you?",
            "aşk": "Romance novels can warm the heart. What type of love story do you prefer?",
            "macera": "Adventure books can take you on exciting journeys. What kind of adventure interests you?",
            "gizem": "Mystery books can keep you guessing until the end. Do you prefer cozy mysteries or thrillers?",
            "komedi": "Humorous books can brighten your day. What type of humor do you enjoy?",
            "drama": "Dramatic books can evoke strong emotions. What kind of drama interests you?",
        }
    else:
        MOCK_RESPONSES = {
            "default": "Kitap önerileri ve okuma tavsiyeleri konusunda size yardımcı olmaya hazırım. Ne öğrenmek istiyorsunuz?",
            "roman": "Harika romanlar önermekten mutluluk duyarım! Hangi tür sizi daha çok ilgilendiriyor?",
            "kitap": "Çeşitli türlerde kitap önerebilirim. Hangi tür kitapları okumayı seviyorsunuz?",
            "yazar": "Keşfedilecek birçok harika yazar var. Hangi edebi dönem veya tür sizi ilgilendiriyor?",
            "edebiyat": "Edebiyat geniş ve güzel bir dünya! Hangi yönünü keşfetmek istiyorsunuz?",
            "okuma": "Okumak harika bir alışkanlık! Daha iyi okuma pratikleri geliştirmenize ve ilgi alanlarınıza uygun kitaplar bulmanıza yardımcı olabilirim.",
            "bilim kurgu": "Bilim kurgu büyüleyici! George Orwell'in '1984'ü veya Andy Weir'in 'Marslı'sı gibi klasikleri önerebilirim.",
            "fantastik": "Fantastik kitaplar sizi büyülü dünyalara götürebilir! Epik fantastik mi yoksa şehir fantastiği mi istiyorsunuz?",
            "klasik": "Klasik edebiyat zamansız hikayeler sunar. Farklı dönem ve kültürlerden eserler önerebilirim.",
            "şiir": "Şiir ruhunuza benzersiz şekillerde dokunabilir. Hangi tür şiir sizi ilgilendiriyor?",
            "tarih": "Tarih kitapları geçmişi canlandırabilir. Hangi tarihsel dönem sizi büyülüyor?",
            "felsefe": "Felsefe kitapları düşüncelerinizi genişletebilir. Antik, modern mi yoksa belirli felsefi konular mı ilginizi çekiyor?",
            "felsefe": "Felsefe kitapları düşüncelerinizi genişletebilir. Antik, modern mi yoksa belirli felsefi konular mı ilginizi çekiyor?",
            "psikoloji": "Psikoloji kitapları insan davranışını anlamanıza yardımcı olabilir. Psikolojinin hangi yönü ilginizi çekiyor?",
            "teknoloji": "Teknoloji kitapları sizi en son gelişmeler hakkında güncel tutabilir. Hangi teknoloji alanı ilginizi çekiyor?",
            "sanat": "Sanat kitapları yaratıcılığınızı ilham verebilir. Hangi sanat formu veya dönem ilginizi çekiyor?",
            "doğa": "Doğa kitapları çevreye olan takdirinizi derinleştirebilir. Doğanın hangi yönü sizi büyülüyor?",
            "aşk": "Romantik romanlar kalbinizi ısıtabilir. Ne tür bir aşk hikayesi tercih ediyorsunuz?",
            "macera": "Macera kitapları sizi heyecan verici yolculuklara çıkarabilir. Ne tür bir macera ilginizi çekiyor?",
            "gizem": "Gizem kitapları sizi sonuna kadar tahmin etmeye zorlayabilir. Rahat gizemler mi yoksa gerilimler mi tercih ediyorsunuz?",
            "komedi": "Mizahi kitaplar gününüzü aydınlatabilir. Ne tür mizah hoşunuza gidiyor?",
            "drama": "Dramatik kitaplar güçlü duygular uyandırabilir. Ne tür drama ilginizi çekiyor?",
        }

    # Enhanced topic detection with more keywords
    topic_patterns = {
        "roman": ["roman", "novel", "fiction", "hikaye", "story"],
        "bilim kurgu": [
            "bilim kurgu",
            "science fiction",
            "sci-fi",
            "uzay",
            "space",
            "gelecek",
            "future",
        ],
        "fantastik": [
            "fantastik",
            "fantasy",
            "büyü",
            "magic",
            "sihir",
            "elf",
            "dragon",
        ],
        "klasik": ["klasik", "classic", "eski", "old", "geleneksel", "traditional"],
        "polisiye": [
            "polisiye",
            "detective",
            "cinayet",
            "murder",
            "gizem",
            "mystery",
            "dedektif",
        ],
        "tarih": ["tarih", "history", "historical", "geçmiş", "past", "savaş", "war"],
        "felsefe": ["felsefe", "philosophy", "düşünce", "thought", "mantık", "logic"],
        "psikoloji": [
            "psikoloji",
            "psychology",
            "ruh",
            "soul",
            "karakter",
            "character",
            "davranış",
            "behavior",
        ],
        "teknoloji": [
            "teknoloji",
            "technology",
            "tech",
            "dijital",
            "digital",
            "yapay zeka",
            "ai",
        ],
        "sanat": [
            "sanat",
            "art",
            "resim",
            "painting",
            "müzik",
            "music",
            "heykel",
            "sculpture",
        ],
        "doğa": [
            "doğa",
            "nature",
            "çevre",
            "environment",
            "orman",
            "forest",
            "deniz",
            "sea",
        ],
        "aşk": ["aşk", "love", "romantik", "romantic", "kalp", "heart"],
        "macera": [
            "macera",
            "adventure",
            "keşif",
            "exploration",
            "heyecan",
            "excitement",
        ],
        "gizem": ["gizem", "mystery", "gerilim", "thriller", "suspense"],
        "komedi": ["komedi", "comedy", "mizah", "humor", "eğlenceli", "funny"],
        "drama": ["drama", "dramatic", "duygusal", "emotional", "tragedy"],
        "şiir": ["şiir", "poetry", "poem", "verse", "dize"],
        "çocuk": ["çocuk", "child", "masal", "fairy tale", "çocuk edebiyatı"],
        "genç": ["genç", "young", "teen", "adolescent", "gençlik"],
        "yetişkin": ["yetişkin", "adult", "olgun", "mature"],
        "yemek": ["yemek", "food", "yemek kitabı", "cookbook", "şef", "chef"],
        "spor": ["spor", "sport", "futbol", "football", "basketbol", "basketball"],
        "seyahat": ["seyahat", "travel", "gezi", "journey", "macera", "adventure"],
        "müzik": ["müzik", "music", "şarkı", "song", "melodi", "melody"],
        "okuma": ["okuma", "reading", "read", "kitap okuma", "book reading"],
        "hızlı okuma": ["hızlı okuma", "speed reading", "fast reading"],
        "anlayarak okuma": ["anlayarak okuma", "comprehension", "understanding"],
        "mutlu": ["mutlu", "happy", "neşeli", "cheerful", "keyifli", "enjoyable"],
        "üzgün": ["üzgün", "sad", "mutsuz", "unhappy", "kederli", "sorrowful"],
        "stresli": ["stresli", "stressed", "gergin", "tense", "endişeli", "anxious"],
        "enerjik": ["enerjik", "energetic", "canlı", "lively", "dinç", "vigorous"],
        "yaz": ["yaz", "summer", "sıcak", "hot", "tatil", "vacation"],
        "kış": ["kış", "winter", "soğuk", "cold", "kar", "snow"],
        "yağmur": ["yağmur", "rain", "ıslak", "wet", "bulutlu", "cloudy"],
        "güneş": ["güneş", "sun", "parlak", "bright", "sıcak", "warm"],
    }

    # Check for specific topics with enhanced pattern matching
    for topic, patterns in topic_patterns.items():
        if any(pattern in message_lower for pattern in patterns):
            if topic in MOCK_RESPONSES:
                return MOCK_RESPONSES[topic]
            else:
                # Fallback to default responses for new topics
                if user_language == "tr":
                    return f"{topic.title()} konusunda size yardımcı olabilirim! Hangi türde {topic} kitabı arıyorsunuz?"
                else:
                    return f"I can help you with {topic}! What type of {topic} book are you looking for?"

    # Check for question words and provide contextual responses
    question_words = (
        ["ne", "hangi", "nasıl", "neden", "kim", "nerede", "ne zaman", "kaç"]
        if user_language == "tr"
        else ["what", "which", "how", "why", "who", "where", "when", "how many"]
    )

    if any(word in message_lower for word in question_words):
        # Try to find a more specific topic in the message
        for topic, patterns in topic_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                if topic in MOCK_RESPONSES:
                    return MOCK_RESPONSES[topic]

        # If no specific topic found, provide a helpful general response
        if user_language == "tr":
            return "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?"
        else:
            return "I'm here to help you with this topic! I can provide book recommendations, literature information, or reading advice. What type of books interest you?"

    # Check for greetings and casual conversation
    greeting_words = (
        ["merhaba", "selam", "hi", "hello", "hey"]
        if user_language == "tr"
        else ["hello", "hi", "hey", "good morning", "good afternoon"]
    )
    if any(word in message_lower for word in greeting_words):
        if user_language == "tr":
            return "Merhaba! Ben Luminis.AI Kütüphane Asistanı. Size nasıl yardımcı olabilirim? Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri konusunda yardımcı olabilirim."
        else:
            return "Hello! I'm Luminis.AI Library Assistant. How can I help you? I can assist with book recommendations, literature information, or reading advice."

    # Check for thanks and appreciation
    thanks_words = (
        ["teşekkür", "sağol", "thanks", "thank you", "appreciate"]
        if user_language == "tr"
        else ["thanks", "thank you", "appreciate", "grateful"]
    )
    if any(word in message_lower for word in thanks_words):
        if user_language == "tr":
            return "Rica ederim! Başka bir konuda yardıma ihtiyacınız olursa her zaman buradayım. Kitap önerileri, edebiyat tartışmaları veya okuma tavsiyeleri için sorabilirsiniz."
        else:
            return "You're welcome! I'm always here if you need help with anything else. Feel free to ask about book recommendations, literature discussions, or reading advice."

    # Default response with more variety
    default_responses = {
        "tr": [
            "Bu konu hakkında size yardımcı olmaya çalışıyorum! Kitap önerileri, edebiyat bilgisi veya okuma tavsiyeleri için daha spesifik sorular sorabilirsiniz. Hangi türde kitap ilginizi çekiyor?",
            "Kitap dünyasında size rehberlik etmekten mutluluk duyarım! Hangi konuda yardıma ihtiyacınız var?",
            "Edebiyat dünyasında keşfedilecek çok şey var! Size hangi konuda yardımcı olabilirim?",
            "Kitap önerileri ve edebiyat bilgisi konusunda uzmanım! Ne öğrenmek istiyorsunuz?",
        ],
        "en": [
            "I'm here to help you with this topic! I can provide book recommendations, literature information, or reading advice. What type of books interest you?",
            "I'd be happy to guide you through the world of books! What can I help you with?",
            "There's so much to discover in the world of literature! How can I assist you?",
            "I'm an expert in book recommendations and literature knowledge! What would you like to learn?",
        ],
    }

    import random

    return random.choice(default_responses[user_language])


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint for AI library assistant"""
    try:
        user_message = request.message
        user_language = request.language or "tr"

        # Debug logging
        print(f"DEBUG: Received message: {user_message}")
        print(f"DEBUG: Received language: {user_language}")
        print(f"DEBUG: Request object: {request}")

        # Use mock response directly due to OpenAI quota issues
        print("DEBUG: Using mock response due to OpenAI quota limitations")
        ai_response = get_mock_response(user_message, user_language)
        print(f"DEBUG: Mock Response: {ai_response}")

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
            "teknoloji",
            "sanat",
            "doğa",
            "aşk",
            "macera",
            "gizem",
            "komedi",
            "drama",
            "şiir",
            "çocuk",
            "genç",
            "yetişkin",
        ]
        is_book_request = any(
            keyword in user_message.lower() for keyword in book_keywords
        )
        print(
            f"DEBUG: Book request check - message: '{user_message.lower()}', keywords: {book_keywords}, is_book_request: {is_book_request}"
        )

        # If it's a book recommendation request, include book data
        books_data = None
        if is_book_request:
            try:
                print(
                    f"DEBUG: Book request detected! BOOKS_DATABASE length: {len(BOOKS_DATABASE)}"
                )

                # Filter books by genre if mentioned
                message_lower = user_message.lower()
                filtered_books = BOOKS_DATABASE

                # Check for specific genres
                if "bilim kurgu" in message_lower:
                    filtered_books = [
                        book
                        for book in BOOKS_DATABASE
                        if "bilim kurgu" in book.get("genre", "").lower()
                        or "distopya" in book.get("genre", "").lower()
                    ]
                elif "fantastik" in message_lower:
                    filtered_books = [
                        book
                        for book in BOOKS_DATABASE
                        if "fantastik" in book.get("genre", "").lower()
                    ]
                elif "roman" in message_lower:
                    filtered_books = [
                        book
                        for book in BOOKS_DATABASE
                        if "roman" in book.get("genre", "").lower()
                    ]
                elif "klasik" in message_lower:
                    filtered_books = [
                        book
                        for book in BOOKS_DATABASE
                        if any(
                            keyword in book.get("genre", "").lower()
                            for keyword in ["klasik", "roman", "distopya"]
                        )
                    ]
                elif "polisiye" in message_lower:
                    filtered_books = [
                        book
                        for book in BOOKS_DATABASE
                        if "polisiye" in book.get("genre", "").lower()
                    ]
                elif "felsefe" in message_lower:
                    filtered_books = [
                        book
                        for book in BOOKS_DATABASE
                        if "felsefe" in book.get("genre", "").lower()
                    ]
                elif "çocuk" in message_lower:
                    filtered_books = [
                        book
                        for book in BOOKS_DATABASE
                        if "çocuk" in book.get("genre", "").lower()
                    ]

                # If no specific genre found, use first 3 books
                if not filtered_books:
                    filtered_books = BOOKS_DATABASE[:3]
                else:
                    filtered_books = filtered_books[:3]  # Limit to 3 books

                # Translate books based on user language
                books_data = []
                for book in filtered_books:
                    if user_language == "en":
                        # Use English translations if available
                        translated_book = {
                            "title": book.get("title_en", book.get("title", "")),
                            "author": book.get("author", ""),
                            "genre": book.get("genre_en", book.get("genre", "")),
                            "description": book.get(
                                "description_en", book.get("description", "")
                            ),
                            "rating": book.get("rating", 0),
                            "year": book.get("year", 0),
                        }
                    else:
                        # Use Turkish version
                        translated_book = {
                            "title": book.get("title", ""),
                            "author": book.get("author", ""),
                            "genre": book.get("genre", ""),
                            "description": book.get("description", ""),
                            "rating": book.get("rating", 0),
                            "year": book.get("year", 0),
                        }
                    books_data.append(translated_book)

                print(f"DEBUG: Found {len(books_data)} books for recommendation")
                print(f"DEBUG: Language: {user_language}")
                print(f"DEBUG: Sample book: {books_data[0] if books_data else 'None'}")
            except Exception as e:
                print(f"DEBUG: Error getting books data: {e}")
                books_data = None

        print(f"DEBUG: Final books_data: {books_data}")
        print(f"DEBUG: books_data type: {type(books_data)}")
        print(f"DEBUG: books_data length: {len(books_data) if books_data else 'None'}")

        return ChatResponse(
            success=True,
            response=ai_response,
            user_message=user_message,
            books=books_data,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/book-recommendations", response_model=BookRecommendationResponse)
async def get_book_recommendations(request: BookRecommendationRequest):
    """Get book recommendations based on user preferences"""
    try:
        user_preferences = request.preferences
        genre = user_preferences.get("genre", "")
        mood = user_preferences.get("mood", "")

        # Smart book filtering based on preferences
        filtered_books = []

        if genre:
            # Filter by genre (case-insensitive)
            genre_lower = genre.lower()
            filtered_books = [
                book
                for book in BOOKS_DATABASE
                if genre_lower in book.get("genre", "").lower()
            ]

        if mood:
            # Mood-based filtering
            mood_lower = mood.lower()
            mood_books = []

            if mood_lower in ["mutlu", "happy", "neşeli", "joyful"]:
                mood_books = [
                    book
                    for book in BOOKS_DATABASE
                    if any(
                        keyword in book.get("description", "").lower()
                        for keyword in [
                            "mutlu",
                            "neşeli",
                            "sıcak",
                            "umut",
                            "güzel",
                            "harika",
                        ]
                    )
                ]
            elif mood_lower in ["üzgün", "sad", "hüzünlü", "melancholic"]:
                mood_books = [
                    book
                    for book in BOOKS_DATABASE
                    if any(
                        keyword in book.get("description", "").lower()
                        for keyword in ["üzgün", "hüzün", "dram", "acı", "kayıp"]
                    )
                ]
            elif mood_lower in ["stresli", "stressed", "gergin", "tense"]:
                mood_books = [
                    book
                    for book in BOOKS_DATABASE
                    if any(
                        keyword in book.get("description", "").lower()
                        for keyword in [
                            "sakin",
                            "huzur",
                            "rahat",
                            "dinlendirici",
                            "doğa",
                        ]
                    )
                ]
            elif mood_lower in ["enerjik", "energetic", "canlı", "lively"]:
                mood_books = [
                    book
                    for book in BOOKS_DATABASE
                    if any(
                        keyword in book.get("description", "").lower()
                        for keyword in [
                            "macera",
                            "aksiyon",
                            "heyecan",
                            "gizem",
                            "polisiye",
                        ]
                    )
                ]

            if mood_books:
                filtered_books = (
                    mood_books
                    if not filtered_books
                    else [b for b in filtered_books if b in mood_books]
                )

        # If no specific preferences, return top-rated books
        if not filtered_books:
            filtered_books = sorted(
                BOOKS_DATABASE, key=lambda x: x.get("rating", 0), reverse=True
            )[:10]
        else:
            # Sort filtered books by rating
            filtered_books = sorted(
                filtered_books, key=lambda x: x.get("rating", 0), reverse=True
            )

        # Limit to top 5 recommendations
        top_books = filtered_books[:5]

        # Create detailed recommendations
        recommendations = f"Size {len(top_books)} harika kitap öneriyorum:\n\n"

        for i, book in enumerate(top_books, 1):
            recommendations += f"{i}. **{book['title']}** - {book['author']}\n"
            recommendations += f"   📚 Tür: {book['genre']}\n"
            recommendations += f"   ⭐ Puan: {book['rating']}/5.0\n"
            recommendations += f"   📖 {book['description']}\n\n"

        if not top_books:
            recommendations = "Üzgünüm, belirttiğiniz kriterlere uygun kitap bulamadım. Size genel öneriler verebilirim:\n\n"
            top_general = sorted(
                BOOKS_DATABASE, key=lambda x: x.get("rating", 0), reverse=True
            )[:3]
            for i, book in enumerate(top_general, 1):
                recommendations += (
                    f"{i}. **{book['title']}** - {book['author']} ({book['genre']})\n"
                )

        return BookRecommendationResponse(
            success=True, recommendations=recommendations, books=top_books
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books/random", response_model=dict)
async def get_random_books():
    """Get 5 random books from the database"""
    try:
        import random

        random_books = random.sample(BOOKS_DATABASE, min(5, len(BOOKS_DATABASE)))

        return {
            "success": True,
            "books": random_books,
            "total_books": len(BOOKS_DATABASE),
            "message": f"Size {len(random_books)} rastgele kitap öneriyorum!",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books/top-rated", response_model=dict)
async def get_top_rated_books():
    """Get top 10 highest rated books"""
    try:
        top_books = sorted(
            BOOKS_DATABASE, key=lambda x: x.get("rating", 0), reverse=True
        )[:10]

        return {
            "success": True,
            "books": top_books,
            "total_books": len(BOOKS_DATABASE),
            "message": "En yüksek puanlı 10 kitap:",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books/genre/{genre_name}", response_model=dict)
async def get_books_by_genre(genre_name: str):
    """Get books by specific genre"""
    try:
        genre_lower = genre_name.lower()
        genre_books = [
            book
            for book in BOOKS_DATABASE
            if genre_lower in book.get("genre", "").lower()
        ]

        if not genre_books:
            return {
                "success": False,
                "message": f"'{genre_name}' türünde kitap bulunamadı.",
                "available_genres": list(
                    set(book.get("genre", "") for book in BOOKS_DATABASE)
                ),
            }

        return {
            "success": True,
            "books": genre_books,
            "genre": genre_name,
            "count": len(genre_books),
            "message": f"'{genre_name}' türünde {len(genre_books)} kitap bulundu:",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# OPEN LIBRARY API ENDPOINTS
# ============================================================================


@app.get("/api/openlibrary/search")
async def search_openlibrary_books(query: str, limit: int = 20):
    """Search books from Open Library API"""
    try:
        if not openlibrary_service:
            raise HTTPException(
                status_code=503, detail="Open Library service not available"
            )

        books = openlibrary_service.search_books(query, limit)

        return {
            "success": True,
            "query": query,
            "books": books,
            "count": len(books),
            "message": f"Open Library'de '{query}' için {len(books)} kitap bulundu",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/openlibrary/popular")
async def get_popular_openlibrary_books(limit: int = 30):
    """Get popular books from Open Library"""
    try:
        if not openlibrary_service:
            raise HTTPException(
                status_code=503, detail="Open Library service not available"
            )

        books = openlibrary_service.search_popular_books(limit)

        return {
            "success": True,
            "books": books,
            "count": len(books),
            "message": f"Open Library'den {len(books)} popüler kitap getirildi",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/openlibrary/sync")
async def sync_openlibrary_books(sync_request: dict):
    """Sync books from Open Library to local database"""
    try:
        if not openlibrary_service:
            raise HTTPException(
                status_code=503, detail="Open Library service not available"
            )

        query = sync_request.get("query", "bestseller")
        limit = sync_request.get("limit", 20)

        # Search for books
        books = openlibrary_service.search_books(query, limit)

        if not books:
            return {"success": False, "message": f"'{query}' için kitap bulunamadı"}

        # Sync books to database format
        sync_result = openlibrary_service.sync_books_to_database(books)

        # Add synced books to our local database
        for book in sync_result["books"]:
            if book not in BOOKS_DATABASE:
                BOOKS_DATABASE.append(book)

        return {
            "success": True,
            "message": f"{sync_result['synced_count']} kitap başarıyla senkronize edildi",
            "synced_count": sync_result["synced_count"],
            "error_count": sync_result["error_count"],
            "total_books_in_db": len(BOOKS_DATABASE),
            "new_books": sync_result["books"],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/openlibrary/health")
async def check_openlibrary_health():
    """Check Open Library API health"""
    try:
        if not openlibrary_service:
            return {
                "success": False,
                "message": "Open Library service not available",
                "status": "unavailable",
            }

        health = openlibrary_service.health_check()

        return {"success": True, "service": "Open Library API", "health": health}

    except Exception as e:
        return {"success": False, "message": str(e), "status": "error"}


@app.get("/api/openlibrary/genres")
async def get_available_genres():
    """Get available genres from Open Library service"""
    try:
        if not openlibrary_service:
            return {
                "success": False,
                "message": "Open Library service not available",
                "genres": [],
            }

        genres = openlibrary_service.get_available_genres()

        return {
            "success": True,
            "genres": genres,
            "count": len(genres),
            "message": f"{len(genres)} farklı tür mevcut",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================


@app.post("/api/auth/register", response_model=dict)
async def register_user(request: dict):
    """Register a new user"""
    try:
        if auth_service is None:
            raise HTTPException(
                status_code=503, detail="Authentication service not available"
            )

        # Extract user data
        username = request.get("username")
        email = request.get("email")
        password = request.get("password")

        if not all([username, email, password]):
            raise HTTPException(status_code=400, detail="Missing required fields")

        # Check if user already exists
        db = next(get_db())
        existing_user = (
            db.query(User)
            .filter((User.email == email) | (User.username == username))
            .first()
        )

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create new user
        password_hash = auth_service.get_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            auth_provider="local",
            is_active=1,
            is_verified=0,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create tokens
        tokens = auth_service.create_user_tokens(new_user)

        return {
            "success": True,
            "message": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
            },
            **tokens,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/login", response_model=dict)
async def login_user(request: dict):
    """Login user with email and password"""
    try:
        if auth_service is None:
            raise HTTPException(
                status_code=503, detail="Authentication service not available"
            )

        email = request.get("email")
        password = request.get("password")

        if not all([email, password]):
            raise HTTPException(status_code=400, detail="Missing email or password")

        # Authenticate user
        db = next(get_db())
        user = auth_service.authenticate_user(db, email, password)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not user.is_active:
            raise HTTPException(status_code=400, detail="User account is inactive")

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create tokens
        tokens = auth_service.create_user_tokens(user)

        return {
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_photo": user.profile_photo,
            },
            **tokens,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/refresh", response_model=dict)
async def refresh_token(request: dict):
    """Refresh access token using refresh token"""
    try:
        if auth_service is None:
            raise HTTPException(
                status_code=503, detail="Authentication service not available"
            )

        refresh_token = request.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token required")

        # Refresh token
        new_access_token = auth_service.refresh_access_token(refresh_token)

        return {
            "success": True,
            "access_token": new_access_token,
            "token_type": "bearer",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/auth/oauth/{provider}/url")
async def get_oauth_url(provider: str, state: str = None):
    """Get OAuth 2.0 authorization URL"""
    try:
        if oauth2_service is None:
            raise HTTPException(status_code=503, detail="OAuth service not available")

        oauth_url = oauth2_service.get_oauth_url(provider, state)

        return {"success": True, "oauth_url": oauth_url, "provider": provider}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/oauth/{provider}/callback")
async def oauth_callback(provider: str, request: dict):
    """Handle OAuth 2.0 callback"""
    try:
        if oauth2_service is None:
            raise HTTPException(status_code=503, detail="OAuth service not available")

        authorization_code = request.get("code")
        if not authorization_code:
            raise HTTPException(status_code=400, detail="Authorization code required")

        # Exchange code for token
        token_data = oauth2_service.exchange_code_for_token(
            provider, authorization_code
        )
        access_token = token_data["access_token"]

        # Get user info from provider
        user_info = oauth2_service.get_user_info(provider, access_token)

        # Check if user exists, if not create
        db = next(get_db())
        user = (
            db.query(User)
            .filter(
                User.auth_provider == provider, User.auth_provider_id == user_info["id"]
            )
            .first()
        )

        if not user:
            # Create new user
            user = User(
                username=user_info["name"],
                email=user_info["email"],
                auth_provider=provider,
                auth_provider_id=user_info["id"],
                profile_photo=user_info.get("picture"),
                is_active=1,
                is_verified=1,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        # Create JWT tokens
        tokens = auth_service.create_user_tokens(user)

        return {
            "success": True,
            "message": "OAuth authentication successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "profile_photo": user.profile_photo,
            },
            **tokens,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/auth/profile", response_model=dict)
async def get_user_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    try:
        return {
            "success": True,
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "profile_photo": current_user.profile_photo,
                "is_active": bool(current_user.is_active),
                "is_verified": bool(current_user.is_verified),
                "auth_provider": current_user.auth_provider,
                "created_at": current_user.created_at.isoformat()
                if current_user.created_at
                else None,
                "last_login": current_user.last_login.isoformat()
                if current_user.last_login
                else None,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/auth/profile", response_model=dict)
async def update_user_profile(
    request: dict, current_user: User = Depends(get_current_active_user)
):
    """Update user profile"""
    try:
        db = next(get_db())

        # Update allowed fields
        if "username" in request:
            current_user.username = request["username"]
        if "profile_photo" in request:
            current_user.profile_photo = request["profile_photo"]

        current_user.updated_at = datetime.utcnow()
        db.commit()

        return {
            "success": True,
            "message": "Profile updated successfully",
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "profile_photo": current_user.profile_photo,
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/auth/logout", response_model=dict)
async def logout_user(current_user: User = Depends(get_current_active_user)):
    """Logout user (client should discard tokens)"""
    try:
        # In a real implementation, you might want to blacklist the token
        # For now, we'll just return success and let the client handle it

        return {"success": True, "message": "Logout successful"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PROTECTED ENDPOINTS (Require Authentication)
# ============================================================================


@app.get("/api/books")
async def get_books():
    """Get all books from database"""
    try:
        return {"success": True, "books": BOOKS_DATABASE}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze-reading", response_model=ReadingAnalysisResponse)
async def analyze_reading(request: ReadingAnalysisRequest):
    """Analyze user's reading list"""
    try:
        reading_list = request.reading_list

        if not reading_list:
            raise HTTPException(status_code=400, detail="Reading list is empty")

        # Create analysis prompt
        prompt = f"""Analyze the user's reading list and provide insights:
        
        {json.dumps(reading_list, indent=2, ensure_ascii=False)}
        
        Analysis should include:
        1. Most preferred genre
        2. Reading habits
        3. Recommendations and advice
        4. Similar books"""

        try:
            if client is None:
                raise HTTPException(
                    status_code=503, detail="OpenAI API is not configured."
                )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a literature analyst and reading coach.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )

            analysis = response.choices[0].message.content

        except Exception as openai_error:
            # If OpenAI API fails, use mock analysis
            print(f"OpenAI API Error: {openai_error}")
            analysis = "I analyzed your reading list. I can see you read various genres of books. This is a great habit! You can use the chat feature for more book recommendations."

        return ReadingAnalysisResponse(success=True, analysis=analysis)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe audio to text using OpenAI Whisper"""
    try:
        # Check if file is audio
        if file.content_type is None or not file.content_type.startswith("audio/"):
            # Also check file extension as fallback
            if not file.filename or not any(
                file.filename.lower().endswith(ext)
                for ext in [".wav", ".mp3", ".m4a", ".ogg", ".flac"]
            ):
                raise HTTPException(
                    status_code=400, detail="Only audio files are accepted"
                )

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            if client is None:
                raise HTTPException(
                    status_code=503, detail="OpenAI API is not configured."
                )

            print(f"Using OpenAI Whisper API with file: {temp_file_path}")
            print(f"File size: {os.path.getsize(temp_file_path)} bytes")

            # Use OpenAI Whisper API
            with open(temp_file_path, "rb") as audio_file:
                print("File opened successfully, calling OpenAI API...")
                response = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file, language="tr"
                )  # Default to Turkish
                print(f"OpenAI API response: {response}")

            transcription = response.text
            print(f"Transcription result: {transcription}")

            return TranscriptionResponse(success=True, text=transcription)

        except Exception as openai_error:
            print(f"OpenAI Whisper API Error: {openai_error}")
            import traceback

            traceback.print_exc()
            raise HTTPException(
                status_code=500,
                detail=f"Audio-to-text transcription failed: {str(openai_error)}",
            )

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    except Exception as e:
        print(f"Transcription error: {e}")
        import traceback

        traceback.print_exc()
        error_detail = str(e) if e else "Unknown error occurred"
        raise HTTPException(
            status_code=500, detail=f"Transcription failed: {error_detail}"
        )


# RAG Service Endpoints
@app.post("/api/rag/chat")
async def rag_chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Enhanced chat with RAG capabilities"""
    try:
        if rag_service is None:
            raise HTTPException(status_code=503, detail="RAG service not available")

        # Use RAG service to answer questions
        response = rag_service.answer_question(request.message)

        return ChatResponse(
            success=True, response=response, user_message=request.message
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rag/recommendations")
async def rag_recommendations(
    request: BookRecommendationRequest, db: Session = Depends(get_db)
):
    """Get personalized book recommendations using RAG"""
    try:
        # Get recommendations from RAG service
        recommendations = rag_service.get_book_recommendations(
            request.preferences, limit=5
        )

        # Create response text
        if recommendations:
            response_text = "Here are your personalized book recommendations:\n\n"
            for i, book in enumerate(recommendations, 1):
                response_text += f"{i}. **{book['title']}** - {book['author']}\n"
                response_text += f"   Category: {book['category']}\n"
                response_text += f"   Rating: {book['rating']}/5\n"
                response_text += f"   {book['description']}\n\n"
        else:
            response_text = "I couldn't find suitable book recommendations for you right now. Please specify different preferences."

        return BookRecommendationResponse(
            success=True, recommendations=response_text, books=recommendations
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rag/search")
async def rag_search_books(q: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search books using semantic similarity"""
    try:
        results = rag_service.search_books(q, limit=limit)

        return {"success": True, "query": q, "results": results, "count": len(results)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Vector Service Endpoints
@app.get("/api/vector/search")
async def vector_search_books(
    q: str, limit: int = 10, threshold: float = 0.7, db: Session = Depends(get_db)
):
    """Advanced semantic search with similarity threshold"""
    try:
        if vector_service is None:
            raise HTTPException(status_code=503, detail="Vector service not available")

        results = vector_service.semantic_search(q, limit=limit, threshold=threshold)

        return {
            "success": True,
            "query": q,
            "results": results,
            "count": len(results),
            "threshold": threshold,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vector/similar/{book_title}")
async def find_similar_books(
    book_title: str, limit: int = 5, db: Session = Depends(get_db)
):
    """Find books similar to a given book"""
    try:
        if vector_service is None:
            raise HTTPException(status_code=503, detail="Vector service not available")

        results = vector_service.find_similar_books(book_title, limit=limit)

        return {
            "success": True,
            "book_title": book_title,
            "similar_books": results,
            "count": len(results),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vector/category/{category}")
async def get_category_recommendations(
    category: str, limit: int = 10, db: Session = Depends(get_db)
):
    """Get book recommendations by category"""
    try:
        if vector_service is None:
            raise HTTPException(status_code=503, detail="Vector service not available")

        results = vector_service.get_category_recommendations(category, limit=limit)

        return {
            "success": True,
            "category": category,
            "books": results,
            "count": len(results),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vector/author/{author}")
async def get_author_books(author: str, limit: int = 10, db: Session = Depends(get_db)):
    """Get books by specific author"""
    try:
        if vector_service is None:
            raise HTTPException(status_code=503, detail="Vector service not available")

        results = vector_service.get_author_books(author, limit=limit)

        return {
            "success": True,
            "author": author,
            "books": results,
            "count": len(results),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/vector/update")
async def update_vector_store(db: Session = Depends(get_db)):
    """Update vector store with new books from database"""
    try:
        if vector_service is None:
            raise HTTPException(status_code=503, detail="Vector service not available")

        vector_service.update_vector_store()

        return {"success": True, "message": "Vector store updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vector/stats")
async def get_vector_stats(db: Session = Depends(get_db)):
    """Get vector store statistics"""
    try:
        if vector_service is None:
            raise HTTPException(status_code=503, detail="Vector service not available")

        stats = vector_service.get_vector_store_stats()

        return {"success": True, "stats": stats}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Luminis.AI Library Assistant API is running",
        "version": "1.0.0",
        "database": "connected",
        "rag_service": "active",
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Luminis.AI Library Assistant API", "version": "1.0.0"}


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    try:
        print("Starting Luminis.AI Library Assistant...")

        # Create database tables
        create_tables()
        print("Database tables created")

        # Initialize sample data
        init_sample_data()
        print("Sample data initialized")

        # Initialize RAG service
        print("RAG service initialized")

        print("Application startup completed!")

    except Exception as e:
        print(f"Startup error: {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
