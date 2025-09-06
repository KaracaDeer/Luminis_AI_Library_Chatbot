#!/usr/bin/env python3
"""
API Examples for Luminis AI Library Assistant

This example demonstrates various API endpoints and their usage
for integrating with the Luminis AI Library Assistant.

Requirements:
- Backend server running on http://localhost:8000
- OpenAI API key configured
"""

import requests
import json
import time
from typing import Dict, List, Optional


class LuminisAPIClient:
    """Comprehensive client for Luminis AI Library Assistant API"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token: Optional[str] = None

    def set_auth_token(self, token: str):
        """Set authentication token for API requests"""
        self.auth_token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    # Health and Status Endpoints
    def health_check(self) -> Dict:
        """Check API health status"""
        return self._make_request("GET", "/api/health")

    def get_status(self) -> Dict:
        """Get API status and version information"""
        return self._make_request("GET", "/api/status")

    # Authentication Endpoints
    def register_user(self, username: str, email: str, password: str) -> Dict:
        """Register a new user"""
        payload = {"username": username, "email": email, "password": password}
        return self._make_request("POST", "/api/auth/register", json=payload)

    def login_user(self, username: str, password: str) -> Dict:
        """Login user and get authentication token"""
        payload = {"username": username, "password": password}
        response = self._make_request("POST", "/api/auth/login", json=payload)

        if "access_token" in response:
            self.set_auth_token(response["access_token"])

        return response

    def get_user_profile(self) -> Dict:
        """Get current user profile"""
        return self._make_request("GET", "/api/auth/profile")

    # Chat Endpoints
    def send_chat_message(self, message: str, chat_history: List[Dict] = None) -> Dict:
        """Send a chat message"""
        payload = {"message": message, "chat_history": chat_history or []}
        return self._make_request("POST", "/api/chat", json=payload)

    def get_chat_history(self, limit: int = 50) -> Dict:
        """Get user's chat history"""
        params = {"limit": limit}
        return self._make_request("GET", "/api/chat/history", params=params)

    # Book Search Endpoints
    def search_books(self, query: str, limit: int = 10) -> Dict:
        """Search for books"""
        params = {"q": query, "limit": limit}
        return self._make_request("GET", "/api/books/search", params=params)

    def get_book_details(self, book_id: str) -> Dict:
        """Get detailed book information"""
        return self._make_request("GET", f"/api/books/{book_id}")

    def get_popular_books(self, limit: int = 10) -> Dict:
        """Get popular books"""
        params = {"limit": limit}
        return self._make_request("GET", "/api/books/popular", params=params)

    def get_books_by_genre(self, genre: str, limit: int = 10) -> Dict:
        """Get books by genre"""
        params = {"limit": limit}
        return self._make_request("GET", f"/api/books/genre/{genre}", params=params)

    # Voice Endpoints
    def transcribe_audio(self, audio_data: str, format: str = "wav") -> Dict:
        """Transcribe audio to text"""
        payload = {"audio_data": audio_data, "format": format}
        return self._make_request("POST", "/api/voice/transcribe", json=payload)

    def voice_chat(self, audio_data: str, format: str = "wav") -> Dict:
        """Send voice input for chat response"""
        payload = {"audio_data": audio_data, "format": format}
        return self._make_request("POST", "/api/voice/chat", json=payload)

    # User Management Endpoints
    def update_profile(self, profile_data: Dict) -> Dict:
        """Update user profile"""
        return self._make_request("PUT", "/api/user/profile", json=profile_data)

    def change_password(self, old_password: str, new_password: str) -> Dict:
        """Change user password"""
        payload = {"old_password": old_password, "new_password": new_password}
        return self._make_request("PUT", "/api/user/password", json=payload)


def demonstrate_api_endpoints():
    """Demonstrate various API endpoints"""

    print("🌐 Luminis AI Library Assistant - API Examples")
    print("=" * 60)

    client = LuminisAPIClient()

    # 1. Health Check
    print("1. Health Check:")
    health = client.health_check()
    print(f"   Status: {'✅ Healthy' if 'error' not in health else '❌ Error'}")
    if "error" not in health:
        print(f"   Response: {health}")
    print()

    # 2. API Status
    print("2. API Status:")
    status = client.get_status()
    if "error" not in status:
        print(f"   Version: {status.get('version', 'Unknown')}")
        print(f"   Environment: {status.get('environment', 'Unknown')}")
        print(f"   Uptime: {status.get('uptime', 'Unknown')}")
    else:
        print(f"   Error: {status['error']}")
    print()

    # 3. User Registration (Example)
    print("3. User Registration (Example):")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
    }
    # Note: This would fail if user already exists, which is expected
    register_response = client.register_user(**register_data)
    if "error" in register_response:
        print(f"   Expected error (user may exist): {register_response['error']}")
    else:
        print(f"   ✅ User registered: {register_response}")
    print()

    # 4. Book Search
    print("4. Book Search:")
    search_results = client.search_books("Python programming", limit=3)
    if "error" not in search_results:
        books = search_results.get("books", [])
        print(f"   Found {len(books)} books:")
        for book in books:
            print(
                f"   • {book.get('title', 'Unknown')} by {book.get('author', 'Unknown')}"
            )
    else:
        print(f"   Error: {search_results['error']}")
    print()

    # 5. Popular Books
    print("5. Popular Books:")
    popular = client.get_popular_books(limit=3)
    if "error" not in popular:
        books = popular.get("books", [])
        print(f"   Found {len(books)} popular books:")
        for book in books:
            print(
                f"   • {book.get('title', 'Unknown')} by {book.get('author', 'Unknown')}"
            )
    else:
        print(f"   Error: {popular['error']}")
    print()

    # 6. Chat Message
    print("6. Chat Message:")
    chat_response = client.send_chat_message("Hello! Can you recommend a good book?")
    if "error" not in chat_response:
        response_text = chat_response.get("response", "No response")
        print(f"   AI Response: {response_text[:100]}...")
    else:
        print(f"   Error: {chat_response['error']}")
    print()


def demonstrate_authentication_flow():
    """Demonstrate user authentication flow"""

    print("🔐 Authentication Flow Example:")
    print("-" * 40)

    client = LuminisAPIClient()

    # 1. Try to login (this will likely fail without valid credentials)
    print("1. Login Attempt:")
    login_response = client.login_user("testuser", "testpassword123")
    if "error" in login_response:
        print(f"   Expected error (invalid credentials): {login_response['error']}")
    else:
        print(f"   ✅ Login successful: {login_response.get('message', 'Success')}")
        print(f"   Token received: {'Yes' if client.auth_token else 'No'}")
    print()

    # 2. Try to get profile (will fail without authentication)
    print("2. Profile Access (without auth):")
    profile = client.get_user_profile()
    if "error" in profile:
        print(f"   Expected error (not authenticated): {profile['error']}")
    else:
        print(f"   Profile: {profile}")
    print()


def demonstrate_error_handling():
    """Demonstrate API error handling"""

    print("⚠️ Error Handling Examples:")
    print("-" * 35)

    client = LuminisAPIClient()

    # 1. Invalid endpoint
    print("1. Invalid Endpoint:")
    response = client._make_request("GET", "/api/invalid/endpoint")
    print(f"   Response: {response}")
    print()

    # 2. Invalid book ID
    print("2. Invalid Book ID:")
    book = client.get_book_details("invalid-id")
    print(f"   Response: {book}")
    print()

    # 3. Empty search query
    print("3. Empty Search Query:")
    search = client.search_books("", limit=5)
    print(f"   Response: {search}")
    print()


def main():
    """Main function to run all API examples"""

    try:
        # Run all demonstrations
        demonstrate_api_endpoints()
        demonstrate_authentication_flow()
        demonstrate_error_handling()

        print("🎉 API Examples completed!")
        print("\n💡 Tips:")
        print("   • Make sure the backend server is running on http://localhost:8000")
        print("   • Check the API documentation for more endpoints")
        print("   • Use proper authentication for protected endpoints")
        print("   • Handle errors gracefully in your applications")

    except Exception as e:
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    main()
