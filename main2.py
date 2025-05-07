import os
import uuid
import time
import numpy as np
import whisper
import webrtcvad
import pyaudio
import scipy.io.wavfile as wavfile
from dotenv import load_dotenv
from playsound import playsound
from deepgram import DeepgramClient, SpeakOptions

load_dotenv()

# Config
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
SAMPLERATE = 16000
CHANNELS = 1
RESPONSE_MP3 = "response.mp3"

# 🎤 VAD-based Audio Recording
def record_audio(filename, record_seconds=5):
    FORMAT = pyaudio.paInt16
    FRAME_DURATION = 30  # ms
    FRAME_SIZE = int(SAMPLERATE * FRAME_DURATION / 1000)
    BUFFER_SIZE = int(SAMPLERATE / FRAME_SIZE * record_seconds)

    # vad = webrtcvad.Vad(2)  # Aggressiveness 0–3
    vad = webrtcvad.Vad(1)
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=CHANNELS, rate=SAMPLERATE,
                     input=True, frames_per_buffer=FRAME_SIZE)

    print("🎤 Listening for voice...")
    ring_buffer = []
    triggered = False
    frames = []

    try:
        while True:
            frame = stream.read(FRAME_SIZE, exception_on_overflow=False)
            is_speech = vad.is_speech(frame, SAMPLERATE)

            if not triggered:
                ring_buffer.append(frame)
                if len(ring_buffer) > BUFFER_SIZE:
                    ring_buffer.pop(0)
                if sum(vad.is_speech(f, SAMPLERATE) for f in ring_buffer) > 0.9 * len(ring_buffer):
                    triggered = True
                    frames.extend(ring_buffer)
                    ring_buffer = []
                    print("🎤 Voice detected. Recording...")
            else:
                frames.append(frame)
                if len(frames) > BUFFER_SIZE:
                    break
        print("🎤 Done recording.")
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

    audio_np = np.frombuffer(b"".join(frames), dtype=np.int16)
    wavfile.write(filename, SAMPLERATE, audio_np)

# 📝 Transcribe with Whisper
def transcribe_audio(filename):
    print("📝 Transcribing...")
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print("🗣️ You said:", result["text"])
    return result["text"]

# 🔊 Speak with Deepgram SDK
def speak_response(text):
    print("🔊 Speaking...")
    try:
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        options = SpeakOptions(model="aura-asteria-en")
        response = deepgram.speak.v("1").save(RESPONSE_MP3, {"text": text}, options)
        playsound(RESPONSE_MP3)
    except Exception as e:
        print("⚠️ Deepgram TTS Error:", e)

# 🤖 Basic Agent Logic
def agent(text):
    text = text.lower()
    if "pda" in text:
        return "PDAs are Program Derived Addresses used in Solana programs."
    elif "anchor" in text:
        return "Anchor is a framework for Solana smart contract development."
    elif "cpi" in text:
        return "CPI stands for Cross-Program Invocation in Solana."
    else:
        return "I'm not sure about that. Try asking about PDAs, CPI calls, or Anchor."

# 🔁 Continuous Loop
def main():
    while True:
        filename = f"live_input_{uuid.uuid4()}.wav"
        record_audio(filename)
        user_input = transcribe_audio(filename)
        response = agent(user_input)
        speak_response(response)
        time.sleep(0.5)

if __name__ == "__main__":
    main()
