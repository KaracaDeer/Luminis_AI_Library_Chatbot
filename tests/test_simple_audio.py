#!/usr/bin/env python3
"""
Simple test for audio transcription
"""

import requests


def test_audio_transcription():
    """Test audio transcription with simple audio file"""
    print("🎤 Testing Audio Transcription...")
    print("=" * 50)

    try:
        # Test with a simple text file first (should fail)
        print("🧪 Testing with text file (should fail)...")
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("Bu bir test metnidir.")

        with open("test.txt", "rb") as f:
            files = {"file": ("test.txt", f, "text/plain")}
            response = requests.post(
                "http://localhost:8000/api/transcribe", files=files
            )

        print(f"Text file test - Status: {response.status_code}")
        print(f"Response: {response.text}")

        # Clean up
        import os

        os.remove("test.txt")

        print("\n" + "=" * 50)
        print("🎵 Testing with audio file...")

        # Test with audio file
        with open("test_speech.wav", "rb") as f:
            files = {"file": ("test_speech.wav", f, "audio/wav")}
            response = requests.post(
                "http://localhost:8000/api/transcribe", files=files
            )

        print(f"Audio file test - Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Transcription: {data.get('text', 'No text')}")
        else:
            print(f"❌ Failed with status {response.status_code}")

    except Exception as e:
        print(f"❌ Test error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_audio_transcription()
