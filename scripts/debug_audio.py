#!/usr/bin/env python3
"""
Debug script for audio transcription
"""

import requests
import json
import os


def debug_audio_transcription():
    """Debug audio transcription with detailed logging"""
    print("🔍 Debugging Audio Transcription...")
    print("=" * 50)

    # Check if audio file exists
    audio_file = "test_speech.wav"
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return

    print(f"✅ Audio file found: {audio_file}")
    print(f"📊 File size: {os.path.getsize(audio_file)} bytes")

    # Test with different content types
    content_types = ["audio/wav", "audio/x-wav", "audio/wave", None]  # No content type

    for content_type in content_types:
        print(f"\n🧪 Testing with content type: {content_type}")

        try:
            if content_type:
                files = {"file": (audio_file, open(audio_file, "rb"), content_type)}
            else:
                files = {"file": (audio_file, open(audio_file, "rb"))}

            response = requests.post(
                "http://localhost:8000/api/transcribe", files=files
            )

            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code == 200:
                data = response.json()
                print(f"✅ Success! Transcription: {data.get('text', 'No text')}")
                break
            else:
                print(f"❌ Failed with status {response.status_code}")

        except Exception as e:
            print(f"❌ Test error: {e}")
            import traceback

            traceback.print_exc()

        finally:
            # Close file
            if "files" in locals() and "file" in files:
                files["file"][1].close()


if __name__ == "__main__":
    debug_audio_transcription()
