#!/usr/bin/env python3
"""
Create a real audio file for testing
"""

import wave
import struct
import numpy as np
import os


def create_real_audio():
    """Create a more realistic audio file"""
    print("🎵 Creating realistic audio file...")

    # Audio parameters
    sample_rate = 16000  # Whisper prefers 16kHz
    duration = 2  # 2 seconds

    # Create a more complex waveform that resembles speech
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples)

    # Create a waveform with multiple frequencies (like speech)
    audio_data = np.zeros(samples)

    # Add multiple frequency components
    frequencies = [200, 400, 600, 800, 1000, 1200, 1400, 1600]
    amplitudes = [0.3, 0.2, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02]

    for freq, amp in zip(frequencies, amplitudes):
        audio_data += amp * np.sin(2 * np.pi * freq * t)

    # Add some noise to make it more realistic
    noise = np.random.normal(0, 0.01, samples)
    audio_data += noise

    # Normalize and convert to 16-bit integers
    audio_data = np.clip(audio_data, -1, 1)
    audio_data = (audio_data * 32767).astype(np.int16)

    # Save as WAV file
    filename = "real_speech.wav"
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

    print(f"✅ Realistic audio file created: {filename}")
    print(f"📊 File size: {os.path.getsize(filename)} bytes")
    print(f"🎵 Duration: {duration} seconds")
    print(f"🔊 Sample rate: {sample_rate} Hz")
    print(f"🎼 Frequencies: {frequencies[:4]}... Hz")

    return filename


if __name__ == "__main__":
    create_real_audio()
