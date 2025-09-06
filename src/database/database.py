from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./luminis_library.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)


def get_db() -> Generator:
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def init_sample_data() -> None:
    create_tables()
    # Minimal seed to satisfy tests; extend with real data if needed
    database_session = SessionLocal()
    try:
        # Ensure at least one user exists for sanity checks
        if database_session.query(User).first() is None:
            demo = User(username="demo", email="demo@example.com")
            database_session.add(demo)
            database_session.commit()
    finally:
        database_session.close()


"""
Database Models and Configuration for Luminis.AI Library Assistant
===============================================================

This module defines the database schema, models, and configuration for the
Luminis.AI Library Assistant application. It provides a complete data layer
for user management, book tracking, and chat history.

Database Architecture:
- SQLAlchemy ORM for database operations
- SQLite for development/testing, configurable for production
- Relational database design with proper foreign key relationships
- Enum-based status tracking for book states
- Timestamp tracking for audit and analytics

Core Models:
1. User: User account management with OAuth support
2. Book: Book catalog with metadata and categorization
3. UserBook: User-book relationships with status tracking
4. ChatHistory: Conversation history for AI interactions

Key Features:
- Multi-provider authentication (local, Google, GitHub, Microsoft)
- Flexible book status management (reading, completed, wishlist)
- Comprehensive user profile system
- Chat history tracking for AI learning
- Multi-language book support
- Rating and review system

Database Relationships:
- Users can have multiple books (UserBook junction table)
- Books can belong to multiple users
- Chat history is linked to specific users
- Proper indexing for performance optimization

Configuration:
- Environment-based database URL configuration
- SQLite default for development
- PostgreSQL/MySQL support for production
- Automatic table creation and migration

This module is essential for:
- User account management and authentication
- Book catalog and recommendation systems
- Reading progress tracking
- AI conversation history
- Data persistence and retrieval
- Application state management
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv
import enum

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./luminis_library.db')  # Use SQLite for testing

# For Docker container, use absolute path
if os.path.exists('/app/luminis_library.db'):
    DATABASE_URL = 'sqlite:////app/luminis_library.db'
    print(f"DEBUG: Using Docker database path: {DATABASE_URL}")
else:
    print(f"DEBUG: Using local database path: {DATABASE_URL}")

# Force SQLite for development
if 'mysql' in DATABASE_URL.lower():
    print("WARNING: MySQL detected, switching to SQLite for development")
    DATABASE_URL = 'sqlite:///./luminis_library.db'

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


# Enums
class BookStatus(enum.Enum):
    READING = "reading"
    COMPLETED = "completed"
    WISHLIST = "wishlist"


# Database Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth users
    profile_photo = Column(String(255), nullable=True)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    is_verified = Column(Integer, default=0)  # 1 for verified, 0 for unverified
    auth_provider = Column(String(20), nullable=True)  # "local", "google", "github", "microsoft"
    auth_provider_id = Column(String(100), nullable=True)  # ID from OAuth provider
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    books = relationship("UserBook", back_populates="user")
    chat_history = relationship("ChatHistory", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    isbn = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    language = Column(String(10), default="tr")
    rating = Column(Float, default=0.0)
    year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user_books = relationship("UserBook", back_populates="book")


class UserBook(Base):
    __tablename__ = "user_books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    status = Column(Enum(BookStatus), default=BookStatus.WISHLIST)
    rating = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    added_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="books")
    book = relationship("Book", back_populates="user_books")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_history")


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)


# Initialize database with sample data
def init_sample_data():
    db = SessionLocal()
    try:
        # Check if books already exist
        existing_books = db.query(Book).count()
        if existing_books == 0:
            # Sample books from the original database
            sample_books = [
                {
                    "title": "Suç ve Ceza",
                    "author": "Fyodor Dostoyevski",
                    "category": "Roman",
                    "description": "Psikolojik gerilim ve ahlaki sorgulama",
                    "rating": 4.8,
                    "year": 1866,
                    "language": "tr",
                },
                {
                    "title": "1984",
                    "author": "George Orwell",
                    "category": "Distopya",
                    "description": "Totaliter rejim eleştirisi",
                    "rating": 4.7,
                    "year": 1949,
                    "language": "tr",
                },
                {
                    "title": "Küçük Prens",
                    "author": "Antoine de Saint-Exupéry",
                    "category": "Çocuk Edebiyatı",
                    "description": "Felsefi masal",
                    "rating": 4.9,
                    "year": 1943,
                    "language": "tr",
                },
                {
                    "title": "Dune",
                    "author": "Frank Herbert",
                    "category": "Bilim Kurgu",
                    "description": "Epik bilim kurgu romanı",
                    "rating": 4.6,
                    "year": 1965,
                    "language": "tr",
                },
                {
                    "title": "Hobbit",
                    "author": "J.R.R. Tolkien",
                    "category": "Fantastik",
                    "description": "Orta Dünya macerası",
                    "rating": 4.8,
                    "year": 1937,
                    "language": "tr",
                },
            ]

            for book_data in sample_books:
                book = Book(**book_data)
                db.add(book)

            db.commit()
            print("Sample books added to database")
        else:
            print("Books already exist in database")

    except Exception as e:
        print(f"Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()
