"""
Open Library API Service


This service fetches book data from the Open Library API and integrates it with our local database.
It provides functions to search books, fetch book details, and sync data.
"""

import requests
import json
import time
from typing import List, Dict, Optional, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenLibraryService:
    """Service for interacting with Open Library API"""

    def __init__(self):
        self.base_url = "https://openlibrary.org"
        self.search_url = f"{self.base_url}/search.json"
        self.works_url = f"{self.base_url}/works"
        self.books_url = f"{self.base_url}/books"

    def search_books(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for books using Open Library API

        Args:
            query (str): Search query (title, author, subject)
            limit (int): Maximum number of results

        Returns:
            List[Dict]: List of book search results
        """
        try:
            params = {
                "q": query,
                "limit": limit,
                "fields": "key,title,author_name,first_sentence,subject,language,first_publish_year,edition_count",
            }

            response = requests.get(self.search_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            books = []

            for doc in data.get("docs", []):
                book = {
                    "key": doc.get("key"),
                    "title": doc.get("title"),
                    "author_name": doc.get("author_name", []),
                    "first_sentence": doc.get("first_sentence", []),
                    "subject": doc.get("subject", []),
                    "language": doc.get("language", []),
                    "first_publish_year": doc.get("first_publish_year"),
                    "edition_count": doc.get("edition_count", 0),
                }
                books.append(book)

            logger.info(f"Found {len(books)} books for query: {query}")
            return books

        except requests.RequestException as e:
            logger.error(f"Error searching books: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in search_books: {e}")
            return []

    def get_book_details(self, work_key: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific book

        Args:
            work_key (str): Open Library work key

        Returns:
            Dict: Detailed book information
        """
        try:
            url = f"{self.works_url}/{work_key}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Extract book details
            book_details = {
                "key": work_key,
                "title": data.get("title"),
                "author_name": [],
                "description": "",
                "subjects": [],
                "genres": [],
                "languages": [],
                "first_publish_date": data.get("first_publish_date"),
                "publish_date": data.get("publish_date"),
                "number_of_pages_median": data.get("number_of_pages_median"),
                "rating": {
                    "average": data.get("rating", {}).get("average", 0),
                    "count": data.get("rating", {}).get("count", 0),
                },
            }

            # Extract author information
            if "authors" in data:
                for author in data["authors"]:
                    if "author" in author:
                        author_key = author["author"]["key"]
                        author_name = self._get_author_name(author_key)
                        if author_name:
                            book_details["author_name"].append(author_name)

            # Extract description
            if "description" in data:
                if isinstance(data["description"], dict):
                    book_details["description"] = data["description"].get("value", "")
                else:
                    book_details["description"] = str(data["description"])

            # Extract subjects and genres
            if "subjects" in data:
                book_details["subjects"] = data["subjects"]
                # Map subjects to genres
                book_details["genres"] = self._map_subjects_to_genres(data["subjects"])

            # Extract languages
            if "languages" in data:
                for lang in data["languages"]:
                    if "key" in lang:
                        lang_key = lang["key"]
                        lang_name = self._get_language_name(lang_key)
                        if lang_name:
                            book_details["languages"].append(lang_name)

            logger.info(f"Retrieved details for book: {book_details['title']}")
            return book_details

        except requests.RequestException as e:
            logger.error(f"Error getting book details: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_book_details: {e}")
            return None

    def _get_author_name(self, author_key: str) -> Optional[str]:
        """Get author name from author key"""
        try:
            url = f"{self.base_url}{author_key}.json"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            return data.get("name")

        except Exception as e:
            logger.warning(f"Could not fetch author name for {author_key}: {e}")
            return None

    def _get_language_name(self, lang_key: str) -> Optional[str]:
        """Get language name from language key"""
        try:
            url = f"{self.base_url}{lang_key}.json"
            response = requests.get(url, timeout=5)
            response.raise_for_status()

            data = response.json()
            return data.get("name")

        except Exception as e:
            logger.warning(f"Could not fetch language name for {lang_key}: {e}")
            return None

    def _map_subjects_to_genres(self, subjects: List[str]) -> List[str]:
        """Map Open Library subjects to our genre categories"""
        genre_mapping = {
            "fiction": "Roman",
            "science fiction": "Bilim Kurgu",
            "fantasy": "Fantastik",
            "mystery": "Polisiye",
            "thriller": "Gerilim",
            "romance": "Romantik",
            "historical fiction": "Tarihi Roman",
            "biography": "Biyografi",
            "autobiography": "Otobiyografi",
            "philosophy": "Felsefe",
            "psychology": "Psikoloji",
            "science": "Bilim",
            "technology": "Teknoloji",
            "history": "Tarih",
            "politics": "Politika",
            "economics": "Ekonomi",
            "poetry": "Şiir",
            "drama": "Tiyatro",
            "children": "Çocuk Edebiyatı",
            "young adult": "Gençlik Edebiyatı",
            "cookbooks": "Yemek",
            "travel": "Seyahat",
            "sports": "Spor",
            "music": "Müzik",
            "art": "Sanat",
            "religion": "Din",
            "self-help": "Kişisel Gelişim",
        }

        genres = []
        for subject in subjects:
            subject_lower = subject.lower()
            for key, genre in genre_mapping.items():
                if key in subject_lower:
                    if genre not in genres:
                        genres.append(genre)

        return genres if genres else ["Genel"]

    def search_popular_books(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for popular books by various criteria

        Args:
            limit (int): Maximum number of results

        Returns:
            List[Dict]: List of popular books
        """
        popular_queries = [
            "bestseller",
            "classic literature",
            "award winning",
            "popular fiction",
            "best books",
            "must read",
            "literary fiction",
            "contemporary literature",
        ]

        all_books = []

        for query in popular_queries:
            books = self.search_books(query, limit=limit // len(popular_queries))
            all_books.extend(books)

            # Rate limiting to be respectful to the API
            time.sleep(0.5)

        # Remove duplicates based on key
        unique_books = {}
        for book in all_books:
            if book["key"] not in unique_books:
                unique_books[book["key"]] = book

        return list(unique_books.values())[:limit]

    def sync_books_to_database(self, books: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Sync books from Open Library to our local database format

        Args:
            books (List[Dict]): List of books from Open Library

        Returns:
            Dict: Sync results and statistics
        """
        synced_books = []
        errors = []

        for book in books:
            try:
                # Get detailed book information
                if "key" in book:
                    details = self.get_book_details(book["key"])
                    if details:
                        # Convert to our database format
                        db_book = self._convert_to_db_format(details)
                        if db_book:
                            synced_books.append(db_book)

                # Rate limiting
                time.sleep(0.2)

            except Exception as e:
                errors.append(f"Error syncing book {book.get('title', 'Unknown')}: {e}")

        return {
            "success": True,
            "synced_count": len(synced_books),
            "error_count": len(errors),
            "books": synced_books,
            "errors": errors,
        }

    def _convert_to_db_format(
        self, book_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Convert Open Library book data to our database format"""
        try:
            # Extract author name
            author = book_data.get("author_name", ["Unknown Author"])
            author_str = author[0] if author else "Unknown Author"

            # Extract genre
            genres = book_data.get("genres", ["Genel"])
            genre_str = genres[0] if genres else "Genel"

            # Extract description
            description = book_data.get("description", "")
            if not description and book_data.get("first_sentence"):
                description = (
                    book_data["first_sentence"][0]
                    if book_data["first_sentence"]
                    else "Açıklama mevcut değil"
                )

            # Extract year
            year = book_data.get("first_publish_date")
            if year and isinstance(year, str):
                try:
                    year = int(year.split("-")[0])
                except:
                    year = None

            # Extract rating
            rating = book_data.get("rating", {}).get("average", 0)
            if rating:
                rating = round(float(rating), 1)
            else:
                rating = 4.0

            db_book = {
                "title": book_data.get("title", "Unknown Title"),
                "author": author_str,
                "genre": genre_str,
                "description": description[:500]
                if description
                else "Açıklama mevcut değil",  # Limit description length
                "rating": rating,
                "year": year,
                "openlibrary_key": book_data.get("key"),
                "source": "openlibrary",
                "synced_at": datetime.now().isoformat(),
            }

            return db_book

        except Exception as e:
            logger.error(f"Error converting book to DB format: {e}")
            return None

    def get_available_genres(self) -> List[str]:
        """Get list of available genres from our mapping"""
        return list(
            set(
                [
                    "Roman",
                    "Bilim Kurgu",
                    "Fantastik",
                    "Polisiye",
                    "Gerilim",
                    "Romantik",
                    "Tarihi Roman",
                    "Biyografi",
                    "Otobiyografi",
                    "Felsefe",
                    "Psikoloji",
                    "Bilim",
                    "Teknoloji",
                    "Tarih",
                    "Politika",
                    "Ekonomi",
                    "Şiir",
                    "Tiyatro",
                    "Çocuk Edebiyatı",
                    "Gençlik Edebiyatı",
                    "Yemek",
                    "Seyahat",
                    "Spor",
                    "Müzik",
                    "Sanat",
                    "Din",
                    "Kişisel Gelişim",
                    "Genel",
                ]
            )
        )

    def health_check(self) -> Dict[str, Any]:
        """Check if Open Library API is accessible"""
        try:
            response = requests.get(
                f"{self.base_url}/search.json?q=test&limit=1", timeout=5
            )
            return {
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "status_code": response.status_code,
            }
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
