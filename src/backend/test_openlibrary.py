"""
Test script for Open Library API integration

This script tests the Open Library service and endpoints.
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"


def test_openlibrary_health():
    """Test Open Library API health check"""
    print("🔍 Testing Open Library health...")

    try:
        response = requests.get(f"{BASE_URL}/api/openlibrary/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_openlibrary_search():
    """Test Open Library book search"""
    print("\n🔍 Testing Open Library book search...")

    try:
        response = requests.get(
            f"{BASE_URL}/api/openlibrary/search",
            params={"query": "harry potter", "limit": 5},
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {data.get('count', 0)} books")
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_openlibrary_popular():
    """Test Open Library popular books"""
    print("\n🔍 Testing Open Library popular books...")

    try:
        response = requests.get(
            f"{BASE_URL}/api/openlibrary/popular", params={"limit": 10}
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {data.get('count', 0)} popular books")
        print(f"Response: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_openlibrary_sync():
    """Test Open Library book sync"""
    print("\n🔍 Testing Open Library book sync...")

    try:
        sync_data = {"query": "classic literature", "limit": 5}
        response = requests.post(f"{BASE_URL}/api/openlibrary/sync", json=sync_data)
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Sync result: {json.dumps(data, indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_available_genres():
    """Test available genres endpoint"""
    print("\n🔍 Testing available genres...")

    try:
        response = requests.get(f"{BASE_URL}/api/openlibrary/genres")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Available genres: {data.get('genres', [])}")
        print(f"Total genres: {data.get('count', 0)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_local_database():
    """Test local database after sync"""
    print("\n🔍 Testing local database...")

    try:
        # Test random books
        response = requests.get(f"{BASE_URL}/api/books/random")
        print(f"Random books status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Random books count: {data.get('total_books', 0)}")

        # Test top rated books
        response = requests.get(f"{BASE_URL}/api/books/top-rated")
        print(f"Top rated books status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Top rated books count: {data.get('total_books', 0)}")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Starting Open Library API tests...")
    print("=" * 50)

    tests = [
        ("Health Check", test_openlibrary_health),
        ("Book Search", test_openlibrary_search),
        ("Popular Books", test_openlibrary_popular),
        ("Book Sync", test_openlibrary_sync),
        ("Available Genres", test_available_genres),
        ("Local Database", test_local_database),
    ]

    results = []

    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 30)

        try:
            success = test_func()
            results.append((test_name, success))

            if success:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")

        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))

        # Wait between tests to be respectful to the API
        time.sleep(1)

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Open Library integration is working.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")


if __name__ == "__main__":
    main()
