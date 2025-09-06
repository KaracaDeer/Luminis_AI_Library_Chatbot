#!/usr/bin/env python3
"""
Book Search Example for Luminis AI Library Assistant

This example demonstrates how to search for books and retrieve
book information using the library's search functionality.

Requirements:
- Backend server running on http://localhost:8000
- Database initialized with book data
"""

import requests
import json
from typing import Dict, List, Optional


class BookSearchClient:
    """Client for book search functionality"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def search_books(self, query: str, limit: int = 10) -> Dict:
        """
        Search for books by title, author, or description

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            API response with search results
        """
        url = f"{self.base_url}/api/books/search"

        params = {"q": query, "limit": limit}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_book_by_id(self, book_id: str) -> Dict:
        """
        Get detailed information about a specific book

        Args:
            book_id: Unique book identifier

        Returns:
            API response with book details
        """
        url = f"{self.base_url}/api/books/{book_id}"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_popular_books(self, limit: int = 10) -> Dict:
        """
        Get popular books

        Args:
            limit: Maximum number of results

        Returns:
            API response with popular books
        """
        url = f"{self.base_url}/api/books/popular"

        params = {"limit": limit}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_books_by_genre(self, genre: str, limit: int = 10) -> Dict:
        """
        Get books by genre

        Args:
            genre: Book genre
            limit: Maximum number of results

        Returns:
            API response with books in genre
        """
        url = f"{self.base_url}/api/books/genre/{genre}"

        params = {"limit": limit}

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def get_available_genres(self) -> Dict:
        """
        Get list of available genres

        Returns:
            API response with available genres
        """
        url = f"{self.base_url}/api/books/genres"

        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            return response.status_code == 200
        except:
            return False


def display_book(book: Dict):
    """Display book information in a formatted way"""
    print(f"📖 {book.get('title', 'Unknown Title')}")
    print(f"   👤 Author: {book.get('author', 'Unknown Author')}")
    print(f"   📅 Year: {book.get('publication_year', 'Unknown')}")
    print(f"   🏷️ Genre: {book.get('genre', 'Unknown')}")
    print(f"   📝 Description: {book.get('description', 'No description')[:100]}...")
    print(f"   ⭐ Rating: {book.get('rating', 'N/A')}")
    print("-" * 60)


def display_search_results(results: Dict):
    """Display search results"""
    if "error" in results:
        print(f"❌ Error: {results['error']}")
        return

    books = results.get("books", [])
    total = results.get("total", 0)

    print(f"🔍 Found {total} books:")
    print("=" * 60)

    if not books:
        print("📚 No books found matching your search criteria.")
        return

    for i, book in enumerate(books, 1):
        print(f"{i}. ", end="")
        display_book(book)


def main():
    """Example usage of book search functionality"""

    print("📚 Luminis AI Library Assistant - Book Search Example")
    print("=" * 65)

    # Initialize client
    client = BookSearchClient()

    # Check if API is available
    if not client.health_check():
        print("❌ Error: Backend API is not available!")
        print("Please make sure the backend server is running on http://localhost:8000")
        return

    print("✅ Backend API is available!")
    print("\n📖 Book Search Session")
    print("Commands:")
    print("  'search <query>' - Search for books")
    print("  'popular' - Show popular books")
    print("  'genres' - Show available genres")
    print("  'genre <name>' - Show books by genre")
    print("  'book <id>' - Get book details by ID")
    print("  'quit' - Exit")
    print("-" * 50)

    while True:
        try:
            command = input("\nEnter command: ").strip()

            if command.lower() == "quit":
                print("👋 Goodbye!")
                break

            elif command.lower() == "popular":
                print("🔥 Fetching popular books...")
                results = client.get_popular_books(limit=5)
                display_search_results(results)

            elif command.lower() == "genres":
                print("🏷️ Fetching available genres...")
                response = client.get_available_genres()
                if "error" in response:
                    print(f"❌ Error: {response['error']}")
                else:
                    genres = response.get("genres", [])
                    print(f"📚 Available genres ({len(genres)}):")
                    for genre in genres:
                        print(f"   • {genre}")

            elif command.lower().startswith("genre "):
                genre = command[6:].strip()
                if not genre:
                    print("❌ Please specify a genre name")
                    continue
                print(f"🏷️ Fetching books in genre: {genre}")
                results = client.get_books_by_genre(genre, limit=5)
                display_search_results(results)

            elif command.lower().startswith("book "):
                book_id = command[5:].strip()
                if not book_id:
                    print("❌ Please specify a book ID")
                    continue
                print(f"📖 Fetching book details for ID: {book_id}")
                response = client.get_book_by_id(book_id)
                if "error" in response:
                    print(f"❌ Error: {response['error']}")
                else:
                    book = response.get("book", {})
                    if book:
                        display_book(book)
                    else:
                        print("📚 Book not found")

            elif command.lower().startswith("search "):
                query = command[7:].strip()
                if not query:
                    print("❌ Please specify a search query")
                    continue
                print(f"🔍 Searching for: '{query}'")
                results = client.search_books(query, limit=5)
                display_search_results(results)

            else:
                print(
                    "❓ Unknown command. Use 'search <query>', 'popular', 'genres', 'genre <name>', 'book <id>', or 'quit'"
                )

        except KeyboardInterrupt:
            print("\n\n👋 Search session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")


def example_searches():
    """Example of common book searches"""

    print("\n🔧 Example Book Searches:")
    print("-" * 35)

    client = BookSearchClient()

    # Example searches
    example_queries = [
        "Python programming",
        "machine learning",
        "fiction",
        "science",
        "history",
    ]

    for query in example_queries:
        print(f"\n🔍 Searching for: '{query}'")
        results = client.search_books(query, limit=3)

        if "error" in results:
            print(f"   ❌ Error: {results['error']}")
        else:
            books = results.get("books", [])
            print(f"   📚 Found {len(books)} books")
            for book in books[:2]:  # Show first 2 results
                print(
                    f"   • {book.get('title', 'Unknown')} by {book.get('author', 'Unknown')}"
                )


if __name__ == "__main__":
    # Run the interactive search
    main()

    # Show example searches
    example_searches()
