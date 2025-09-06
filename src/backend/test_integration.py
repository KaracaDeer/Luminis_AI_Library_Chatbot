#!/usr/bin/env python3
"""
Integration Test Script for Luminis AI Library Assistant
Tests MySQL, RAG, and Vector services integration
"""

import sys
import os
import requests
import json
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))


def test_database_connection():
    """Test database connection"""
    print("🔍 Testing database connection...")
    try:
        from database import engine
        from sqlalchemy import text

        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_rag_service():
    """Test RAG service"""
    print("\nTesting RAG service...")
    try:
        # Simple import test for now
        from services.rag_service import RAGService

        print("OK: RAG service import successful")
        return True

    except Exception as e:
        print(f"ERROR: RAG service test failed: {e}")
        return False


def test_vector_service():
    """Test vector service"""
    print("\nTesting vector service...")
    try:
        # Simple import test for now
        from services.vector_service import VectorService

        print("OK: Vector service import successful")
        return True

    except Exception as e:
        print(f"ERROR: Vector service test failed: {e}")
        return False


def test_api_endpoints():
    """Test API endpoints"""
    print("\nTesting API endpoints...")

    # Use Docker/default backend port
    base_url = os.getenv("TEST_BACKEND_URL", "http://localhost:5000")

    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("OK: Health endpoint working")
        else:
            print(f"ERROR: Health endpoint failed: {response.status_code}")
            return False

        # Test chat endpoint (mock-enabled)
        chat_data = {"message": "Merhaba, bana kitap önerir misin?", "language": "tr"}
        response = requests.post(f"{base_url}/api/chat", json=chat_data, timeout=10)
        if response.status_code == 200:
            print("OK: Chat endpoint working")
        else:
            print(f"ERROR: Chat endpoint failed: {response.status_code}")
            return False

        # Optional: vector search endpoint may be disabled without OpenAI
        try:
            response = requests.get(f"{base_url}/api/vector/search?q=roman&limit=3", timeout=10)
            if response.status_code == 200:
                print("OK: Vector search endpoint working")
            else:
                print(f"WARN: Vector search endpoint returned: {response.status_code}")
        except Exception as ve:
            print(f"WARN: Skipping vector search test: {ve}")

        return True

    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def main():
    """Run all integration tests"""
    print("Luminis AI Library Assistant - Integration Tests")
    print("=" * 60)

    tests = [
        ("Database Connection", test_database_connection),
        ("RAG Service", test_rag_service),
        ("Vector Service", test_vector_service),
        ("API Endpoints", test_api_endpoints),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1

    print("=" * 60)
    print(f"Total: {total}, Passed: {passed}, Failed: {total - passed}")

    if passed == total:
        print("All tests passed! Integration successful!")
        return True
    else:
        print("Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
