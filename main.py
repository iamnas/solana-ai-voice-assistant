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
from actions import handle_intent  # Must support passing address
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
    result = model.transcribe(filename, fp16=False)
    print("🗣️ You said:", result["text"])
    return result["text"]

# 🔊 Speak with Deepgram SDK
def speak_response(text):
    try:
        print("🔊 Speaking (with SDK)...")
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)
        TEXT = {"text": text}
        options = SpeakOptions(model="aura-2-asteria-en")
        response = deepgram.speak.rest.v("1").save(RESPONSE_MP3, TEXT, options)
        print("🔊 Playing response...")
        playsound(RESPONSE_MP3)
    except Exception as e:
        print(f"⚠️ Error using Deepgram SDK: {e}")

# 🔐 Prompt for Solana address if needed
def prompt_for_address():
    # speak_response("Please type your Solana wallet address.")
    return input("🔐 Please type your Solana address: ").strip()

# 🧠 Main Loop
def main():
    while True:
        filename = "temp_input.wav"

        record_audio(filename)
        user_input = transcribe_audio(filename)

        if not user_input.strip():
            print("🤖 I didn’t hear anything.")
            speak_response("I didn’t hear anything.")
            continue

        reply, end, intent = agent(user_input, mode="openai")

        extra_data = None
        action_reply = None

        if intent not in [None, "none"] and not end:
            print(f"✨ Detected intent: {intent}")

            if intent in ["get_balance", "get_token_price"]:
                speak_response(reply)
                extra_data = input("🔐 Enter address: ").strip()

            action_reply = handle_intent(intent, extra_data)

        # 🧠 Decide what to speak
        final_reply = action_reply if action_reply else reply
        print("🤖:", final_reply)
        speak_response(final_reply)

        try:
            os.remove(filename)
            if os.path.exists(RESPONSE_MP3):
                os.remove(RESPONSE_MP3)
        except Exception as cleanup_error:
            print(f"⚠️ Cleanup error: {cleanup_error}")

        if end:
            print("👋 Ending conversation.")
            break

        time.sleep(0.5)


if __name__ == "__main__":
    main()

