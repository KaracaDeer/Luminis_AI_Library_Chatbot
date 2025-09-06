#!/usr/bin/env python3
"""
Create a test audio file for testing transcription
"""

import wave
import struct
import numpy as np
import os


def create_test_audio():
    """Create a simple test audio file"""
    print("🎵 Creating test audio file...")

    # Audio parameters
    sample_rate = 16000  # Whisper prefers 16kHz
    duration = 3  # 3 seconds
    frequency = 440  # A4 note

    # Generate audio data (simple sine wave)
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples)

    # Create a more complex waveform (not just pure tone)
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.5
    audio_data += np.sin(2 * np.pi * frequency * 2 * t) * 0.3  # Harmonic
    audio_data += np.sin(2 * np.pi * frequency * 3 * t) * 0.2  # Another harmonic

    # Normalize and convert to 16-bit integers
    audio_data = np.clip(audio_data, -1, 1)
    audio_data = (audio_data * 32767).astype(np.int16)

    # Save as WAV file
    filename = "test_speech.wav"
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

    print(f"✅ Test audio file created: {filename}")
    print(f"📊 File size: {os.path.getsize(filename)} bytes")
    print(f"🎵 Duration: {duration} seconds")
    print(f"🔊 Sample rate: {sample_rate} Hz")

    return filename


if __name__ == "__main__":
    create_test_audio()
