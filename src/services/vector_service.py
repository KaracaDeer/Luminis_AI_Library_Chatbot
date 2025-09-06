"""
Vector Database Service for Luminis.AI Library Assistant
======================================================

This service provides advanced vector database operations for semantic search and
similarity matching in the Luminis.AI Library Assistant. It leverages ChromaDB and
OpenAI embeddings to enable intelligent book discovery and recommendation systems.

Key Features:
1. Semantic Search: Find books based on meaning, not just keywords
2. Similarity Matching: Identify books with similar themes, styles, or content
3. Vector Embeddings: Convert book descriptions to high-dimensional vectors
4. Fast Retrieval: Efficient similarity search using vector databases
5. Dynamic Updates: Automatically update vector store with new books
6. Multi-dimensional Analysis: Consider multiple aspects of books for better matches

Technical Implementation:
- OpenAI Embeddings: Uses text-embedding-ada-002 model for high-quality vectors
- ChromaDB Integration: Persistent vector storage with fast similarity search
- Document Processing: Converts book metadata to searchable vector representations
- Similarity Thresholds: Configurable similarity scores for result filtering
- Batch Operations: Efficient processing of large book collections

Use Cases:
- Finding books similar to user favorites
- Semantic search across book descriptions and content
- Category-based recommendations with similarity scoring
- Author similarity analysis for discovery
- Content-based filtering and ranking

Benefits:
- More accurate book recommendations based on content similarity
- Faster search results compared to traditional text search
- Better understanding of user preferences through similarity patterns
- Scalable architecture for growing book collections
- Reduced manual categorization effort through automatic similarity detection

This service is essential for:
- Advanced book recommendation algorithms
- Content-based filtering systems
- User preference learning and adaptation
- Semantic search capabilities
- Intelligent book discovery workflows
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# Robust database import with fallback mechanisms
try:
    from database.database import SessionLocal, Book, UserBook, BookStatus
except ImportError:
    try:
        from database import SessionLocal, Book, UserBook, BookStatus
    except ImportError:
        # Create dummy classes for testing environments
        print("WARNING: Could not import database module in vector_service.py")

        class DummySessionLocal:
            pass

        class DummyBook:
            pass

        class DummyUserBook:
            pass

        class DummyBookStatus:
            pass

        SessionLocal = DummySessionLocal
        Book = DummyBook
        UserBook = DummyUserBook
        BookStatus = DummyBookStatus
from dotenv import load_dotenv
import numpy as np
from datetime import datetime

# Load environment variables
load_dotenv()


class VectorService:
    def __init__(self):
        """Initialize vector service with ChromaDB"""
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-ada-002")

        self.vector_store = None
        self.persist_directory = "./chroma_db"
        self.collection_name = "luminis_books"

        # Initialize vector store
        self.initialize_vector_store()

    def initialize_vector_store(self):
        """Initialize or load existing ChromaDB vector store"""
        try:
            # Try to load existing vector store
            if os.path.exists(self.persist_directory):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self.embeddings,
                    collection_name=self.collection_name,
                )
                print(f"Loaded existing vector store from {self.persist_directory}")
            else:
                # Create new vector store
                self._create_new_vector_store()

        except Exception as e:
            print(f"Error loading vector store: {e}")
            self._create_new_vector_store()

    def _create_new_vector_store(self):
        """Create new vector store with sample data"""
        try:
            # Load books from database
            db = SessionLocal()
            books = db.query(Book).all()

            if not books:
                print("No books found in database. Creating sample vector store...")
                self._create_sample_vector_store()
                return

            # Convert books to documents with enhanced content
            documents = []
            for book in books:
                # Create rich document content for better embeddings
                content = self._create_book_content(book)

                metadata = {
                    "title": book.title,
                    "author": book.author,
                    "category": book.category,
                    "year": book.year,
                    "language": book.language,
                    "rating": book.rating,
                    "book_id": book.id,
                    "created_at": datetime.utcnow().isoformat(),
                }

                documents.append(Document(page_content=content, metadata=metadata))

            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.persist_directory,
                collection_name=self.collection_name,
            )

            # Persist the vector store
            self.vector_store.persist()

            print(f"Created new vector store with {len(documents)} books")

        except Exception as e:
            print(f"Error creating vector store: {e}")
            self._create_sample_vector_store()
        finally:
            db.close()

    def _create_book_content(self, book: Book) -> str:
        """Create rich content for book embedding"""
        content_parts = [
            f"Kitap Adı: {book.title}",
            f"Yazar: {book.author}",
            f"Kategori: {book.category or 'Genel'}",
            f"Açıklama: {book.description or 'Açıklama yok'}",
            f"Yıl: {book.year or 'Bilinmiyor'}",
            f"Dil: {book.language or 'tr'}",
            f"Puan: {book.rating or 0}",
        ]

        # Add additional context based on category
        if book.category:
            category_context = self._get_category_context(book.category)
            content_parts.append(f"Tür Bilgisi: {category_context}")

        return "\n".join(content_parts)

    def _get_category_context(self, category: str) -> str:
        """Get additional context for book categories"""
        category_contexts = {
            "Roman": "Uzun soluklu, karakter odaklı anlatım",
            "Distopya": "Gelecekteki olumsuz toplum tasviri",
            "Bilim Kurgu": "Teknoloji ve gelecek temalı",
            "Fantastik": "Hayali dünyalar ve büyülü öğeler",
            "Çocuk Edebiyatı": "Çocuklar için eğitici ve eğlenceli",
            "Tarih": "Geçmiş olaylar ve dönemler",
            "Felsefe": "Düşünce ve varoluş sorguları",
            "Psikoloji": "İnsan davranışları ve zihin",
            "Bilim": "Bilimsel keşifler ve araştırmalar",
        }

        return category_contexts.get(category, "Genel edebiyat")

    def _create_sample_vector_store(self):
        """Create sample vector store with enhanced book data"""
        sample_books = [
            {
                "title": "Suç ve Ceza",
                "author": "Fyodor Dostoyevski",
                "category": "Roman",
                "description": "Psikolojik gerilim ve ahlaki sorgulama temalı klasik roman. Raskolnikov'un işlediği cinayet sonrası yaşadığı vicdani azap ve toplumla hesaplaşması",
                "year": 1866,
                "language": "tr",
                "rating": 4.8,
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "category": "Distopya",
                "description": "Totaliter rejim eleştirisi ve distopik toplum analizi. Büyük Birader'in gözetimi altındaki toplumda yaşam",
                "year": 1949,
                "language": "tr",
                "rating": 4.7,
            },
            {
                "title": "Küçük Prens",
                "author": "Antoine de Saint-Exupéry",
                "category": "Çocuk Edebiyatı",
                "description": "Felsefi masal ve hayat dersleri. Küçük prensin farklı gezegenlerdeki yolculuğu ve öğrendiği değerler",
                "year": 1943,
                "language": "tr",
                "rating": 4.9,
            },
            {
                "title": "Dune",
                "author": "Frank Herbert",
                "category": "Bilim Kurgu",
                "description": "Epik bilim kurgu romanı. Arrakis gezegenindeki baharat savaşları ve Paul Atreides'in kaderi",
                "year": 1965,
                "language": "tr",
                "rating": 4.6,
            },
            {
                "title": "Hobbit",
                "author": "J.R.R. Tolkien",
                "category": "Fantastik",
                "description": "Orta Dünya macerası. Bilbo Baggins'in cücelerle birlikte çıktığı tehlikeli yolculuk",
                "year": 1937,
                "language": "tr",
                "rating": 4.8,
            },
        ]

        documents = []
        for book in sample_books:
            content = self._create_book_content_from_dict(book)

            metadata = {
                "title": book["title"],
                "author": book["author"],
                "category": book["category"],
                "year": book["year"],
                "language": book["language"],
                "rating": book["rating"],
                "created_at": datetime.utcnow().isoformat(),
            }

            documents.append(Document(page_content=content, metadata=metadata))

        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
        )

        # Persist the vector store
        self.vector_store.persist()

        print(f"Sample vector store created with {len(documents)} books")

    def _create_book_content_from_dict(self, book: Dict[str, Any]) -> str:
        """Create content from book dictionary"""
        content_parts = [
            f"Kitap Adı: {book['title']}",
            f"Yazar: {book['author']}",
            f"Kategori: {book['category']}",
            f"Açıklama: {book['description']}",
            f"Yıl: {book['year']}",
            f"Dil: {book['language']}",
            f"Puan: {book['rating']}",
        ]

        # Add category context
        category_context = self._get_category_context(book["category"])
        content_parts.append(f"Tür Bilgisi: {category_context}")

        return "\n".join(content_parts)

    def semantic_search(self, query: str, limit: int = 10, threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Advanced semantic search with similarity threshold"""
        try:
            # Search with similarity search
            docs = self.vector_store.similarity_search_with_score(query, k=limit)

            results = []
            for doc, score in docs:
                # Filter by similarity threshold
                if score <= threshold:  # Lower score = higher similarity
                    results.append(
                        {
                            "title": doc.metadata.get("title"),
                            "author": doc.metadata.get("author"),
                            "category": doc.metadata.get("category"),
                            "description": doc.page_content.split("Açıklama: ")[1].split("\n")[0]
                            if "Açıklama: " in doc.page_content
                            else "",
                            "year": doc.metadata.get("year"),
                            "rating": doc.metadata.get("rating"),
                            "similarity_score": 1 - score,  # Convert to similarity score
                            "book_id": doc.metadata.get("book_id"),
                        }
                    )

            # Sort by similarity score
            results.sort(key=lambda x: x["similarity_score"], reverse=True)

            return results

        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []

    def find_similar_books(self, book_title: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find books similar to a given book"""
        try:
            # First, find the book in our database
            db = SessionLocal()
            book = db.query(Book).filter(Book.title.ilike(f"%{book_title}%")).first()

            if not book:
                return []

            # Create query from book content
            query = f"{book.title} {book.author} {book.category} {book.description}"

            # Search for similar books
            similar_books = self.semantic_search(query, limit=limit + 1)  # +1 to exclude the book itself

            # Filter out the book itself
            results = [book for book in similar_books if book["title"] != book_title]

            return results[:limit]

        except Exception as e:
            print(f"Error finding similar books: {e}")
            return []
        finally:
            db.close()

    def get_category_recommendations(self, category: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get book recommendations by category"""
        try:
            query = f"Kategori: {category}"
            return self.semantic_search(query, limit=limit)

        except Exception as e:
            print(f"Error getting category recommendations: {e}")
            return []

    def get_author_books(self, author: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get books by specific author"""
        try:
            query = f"Yazar: {author}"
            return self.semantic_search(query, limit=limit)

        except Exception as e:
            print(f"Error getting author books: {e}")
            return []

    def update_vector_store(self):
        """Update vector store with new books from database"""
        try:
            print("Updating vector store...")
            self._create_new_vector_store()
            print("Vector store updated successfully")

        except Exception as e:
            print(f"Error updating vector store: {e}")

    def get_vector_store_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            if not self.vector_store:
                return {"error": "Vector store not initialized"}

            # Get collection info
            collection = self.vector_store._collection
            count = collection.count()

            return {
                "total_books": count,
                "collection_name": self.collection_name,
                "persist_directory": self.persist_directory,
                "embedding_model": "text-embedding-ada-002",
            }

        except Exception as e:
            return {"error": str(e)}


# Global vector service instance - commented out for testing
# vector_service = VectorService()
