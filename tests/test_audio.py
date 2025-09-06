#!/usr/bin/env python3
"""
Test script for audio transcription endpoint
"""

import requests
import json
import os


def test_audio_transcription():
    """Test the audio transcription endpoint"""
    print("🎤 Testing Audio Transcription Endpoint...")
    print("=" * 50)

    # Test endpoint availability
    try:
        response = requests.get("http://localhost:8000/api/transcribe")
        print(f"GET request status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"GET request error: {e}")

    print("\n" + "=" * 50)
    print("📝 Note: Audio transcription requires a POST request with audio file")
    print("To test with real audio:")
    print("1. Record a short audio message")
    print("2. Save as WAV/MP3 file")
    print("3. Use the /api/transcribe endpoint")
    print("4. The system will convert speech to text using OpenAI Whisper")

    # Test with a simple text file (should fail - audio required)
    print("\n" + "=" * 50)
    print("🧪 Testing with text file (should fail)...")

    try:
        # Create a test text file
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("Bu bir test metnidir.")

        with open("test.txt", "rb") as f:
            files = {"file": ("test.txt", f, "text/plain")}
            response = requests.post("http://localhost:8000/api/transcribe", files=files)

        print(f"POST with text file status: {response.status_code}")
        print(f"Response: {response.text}")

        # Clean up
        os.remove("test.txt")

    except Exception as e:
        print(f"Test error: {e}")


if __name__ == "__main__":
    test_audio_transcription()
