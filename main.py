# main.py

import sounddevice as sd
import os
import time
import numpy as np
import whisper
import scipy.io.wavfile as wavfile
from playsound import playsound
from agent.agent import agent  # Import the agent module
from deepgram import DeepgramClient, SpeakOptions

from dotenv import load_dotenv
load_dotenv()

# Config
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
SAMPLERATE = 16000
CHANNELS = 1
RESPONSE_MP3 = "response.mp3"

# 🎤 Step 1: Record Audio
def record_audio(filename, record_seconds=5):
    print("🎤 Recording...")
    audio = sd.rec(int(record_seconds * SAMPLERATE), samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16')
    sd.wait()
    wavfile.write(filename, SAMPLERATE, audio)
    print("🎤 Done recording.")

# 📝 Step 2: Transcribe Audio
def transcribe_audio(filename):
    print("📝 Transcribing...")
    model = whisper.load_model("base.en")
    result = model.transcribe(filename,fp16=False)
    print("🗣️ You said:", result["text"])
    return result["text"]

# 🔊 Speak with Deepgram SDK
def speak_response(text):
    try:
        print("🔊 Speaking (with SDK)...")
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        TEXT = {"text": text}
        options = SpeakOptions(model="aura-asteria-en")
        # response = deepgram.speak.v("1").save(RESPONSE_MP3, {"text": text}, options)
        response = deepgram.speak.rest.v("1").save(RESPONSE_MP3, TEXT, options)
        print("🔊 Playing response...")
        playsound(RESPONSE_MP3)
    except Exception as e:
        print(f"⚠️ Error using Deepgram SDK: {e}")

# Main Loop
def main():
    while True:
        
        filename = "temp_input.wav"

        
        record_audio(filename)
        user_input = transcribe_audio(filename)

        if not user_input.strip():
            print("🤖 I didn’t hear anything. Would you like to try again or stop the conversation?")
            speak_response('I didn’t hear anything. Would you like to try again or stop the conversation?')
            continue
        

        reply, end = agent(user_input, mode="openai")
        print("response", reply)
        speak_response(reply)

        try:
            os.remove(filename)
            if os.path.exists(RESPONSE_MP3):
                os.remove(RESPONSE_MP3)
        except Exception as cleanup_error:
            print(f"⚠️ Cleanup error: {cleanup_error}")
        
        if end:
            print("👋 Ending conversation as requested by the user.")
            break
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
