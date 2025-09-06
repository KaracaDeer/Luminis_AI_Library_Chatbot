#!/usr/bin/env python3
"""
Voice Recording Example for Luminis AI Library Assistant

This example demonstrates how to record voice input and send it
to the backend for transcription and processing.

Requirements:
- Backend server running on http://localhost:8000
- OpenAI API key configured
- pyaudio library installed (pip install pyaudio)
"""

import requests
import json
import time
import wave
import pyaudio
import io
import base64
from typing import Optional, Dict


class VoiceRecorder:
    """Simple voice recorder for capturing audio input"""

    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio_format = pyaudio.paInt16
        self.channels = 1  # Mono

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

    def record_audio(self, duration: float = 5.0) -> bytes:
        """
        Record audio for specified duration

        Args:
            duration: Recording duration in seconds

        Returns:
            Raw audio data as bytes
        """
        print(f"🎤 Recording for {duration} seconds...")

        # Open stream
        stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        frames = []

        # Record audio
        for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
            data = stream.read(self.chunk_size)
            frames.append(data)

        # Stop recording
        stream.stop_stream()
        stream.close()

        # Combine frames
        audio_data = b''.join(frames)
        print("✅ Recording completed!")

        return audio_data

    def save_audio(self, audio_data: bytes, filename: str):
        """Save audio data to WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.audio_format))
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data)
        print(f"💾 Audio saved to {filename}")

    def close(self):
        """Close the audio interface"""
        self.audio.terminate()


class LuminisVoiceClient:
    """Client for voice interaction with Luminis AI Library Assistant"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def transcribe_audio(self, audio_data: bytes) -> Dict:
        """
        Send audio data for transcription

        Args:
            audio_data: Raw audio data

        Returns:
            API response with transcription
        """
        url = f"{self.base_url}/api/voice/transcribe"

        # Encode audio as base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        payload = {"audio_data": audio_base64, "format": "wav"}

        headers = {"Content-Type": "application/json"}

        try:
            response = self.session.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

    def voice_chat(self, audio_data: bytes, user_id: Optional[str] = None) -> Dict:
        """
        Send voice input for transcription and chat response

        Args:
            audio_data: Raw audio data
            user_id: Optional user ID for authentication

        Returns:
            API response with transcription and chat response
        """
        url = f"{self.base_url}/api/voice/chat"

        # Encode audio as base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        payload = {"audio_data": audio_base64, "format": "wav", "user_id": user_id}

        headers = {"Content-Type": "application/json"}

        try:
            response = self.session.post(url, json=payload, headers=headers)
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


def main():
    """Example usage of voice recording and transcription"""

    print("🎤 Luminis AI Library Assistant - Voice Recording Example")
    print("=" * 65)

    # Initialize components
    recorder = VoiceRecorder()
    client = LuminisVoiceClient()

    # Check if API is available
    if not client.health_check():
        print("❌ Error: Backend API is not available!")
        print("Please make sure the backend server is running on http://localhost:8000")
        return

    print("✅ Backend API is available!")
    print("\n🎙️ Voice Recording Session")
    print("Commands: 'record' to record, 'quit' to exit")
    print("-" * 50)

    try:
        while True:
            command = input("\nEnter command: ").strip().lower()

            if command == 'quit':
                print("👋 Goodbye!")
                break

            elif command == 'record':
                # Record audio
                audio_data = recorder.record_audio(duration=5.0)

                # Save audio file
                timestamp = int(time.time())
                filename = f"voice_recording_{timestamp}.wav"
                recorder.save_audio(audio_data, filename)

                # Send for transcription
                print("🔄 Transcribing audio...")
                response = client.transcribe_audio(audio_data)

                if "error" in response:
                    print(f"❌ Transcription error: {response['error']}")
                else:
                    transcription = response.get("transcription", "No transcription received")
                    print(f"📝 Transcription: {transcription}")

                    # Send for chat response
                    print("🤖 Getting AI response...")
                    chat_response = client.voice_chat(audio_data)

                    if "error" in chat_response:
                        print(f"❌ Chat error: {chat_response['error']}")
                    else:
                        ai_response = chat_response.get("response", "No response received")
                        print(f"🤖 AI Response: {ai_response}")

            else:
                print("❓ Unknown command. Use 'record' or 'quit'")

    except KeyboardInterrupt:
        print("\n\n👋 Voice session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    finally:
        recorder.close()


def example_voice_requests():
    """Example of making direct voice API requests"""

    print("\n🔧 Direct Voice API Request Examples:")
    print("-" * 45)

    # Example: Load and send audio file
    print("1. Audio File Transcription:")
    try:
        # Load a sample audio file (you would replace this with actual audio)
        with open("sample_audio.wav", "rb") as f:
            audio_data = f.read()

        # Encode as base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')

        payload = {"audio_data": audio_base64, "format": "wav"}

        response = requests.post(
            "http://localhost:8000/api/voice/transcribe", json=payload, headers={"Content-Type": "application/json"}
        )

        print(f"   Status: {response.status_code}")
        result = response.json()
        print(f"   Transcription: {result.get('transcription', 'No transcription')}")

    except FileNotFoundError:
        print("   No sample audio file found. Record some audio first!")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    try:
        # Run the interactive voice recording
        main()

        # Show direct API examples
        example_voice_requests()

    except ImportError as e:
        print("❌ Missing required library!")
        print("Please install pyaudio: pip install pyaudio")
        print(f"Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
