import sounddevice as sd
import numpy as np
import whisper
import scipy.io.wavfile as wavfile
import requests
import uuid
import os
from deepgram import DeepgramClient, SpeakOptions

from playsound import playsound

from dotenv import load_dotenv

load_dotenv()

# Config
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")



RECORD_SECONDS = 5
SAMPLERATE = 16000
FILENAME = f"live_input_{uuid.uuid4()}.wav"
RESPONSE_MP3 = "response.mp3"

# 🎤 Step 1: Record Audio
def record_audio(filename):
    print("🎤 Recording...")
    audio = sd.rec(int(RECORD_SECONDS * SAMPLERATE), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    wavfile.write(filename, SAMPLERATE, audio)
    print("🎤 Done recording.")

# 📝 Step 2: Transcribe Audio
def transcribe_audio(filename):
    print("📝 Transcribing...")
    model = whisper.load_model("base.en")
    result = model.transcribe(filename)
    print("🗣️ You said:", result["text"])
    return result["text"]

# # 🔊 Step 3: TTS with Deepgram
# # def speak_response(text):
# #     print("🔊 Speaking...")
# #     response = requests.post(
# #         "https://api.deepgram.com/v1/speak?model=aura-asteria-en",
# #         headers={
# #             "Authorization": f"Token {DEEPGRAM_API_KEY}",
# #             "Content-Type": "application/json"
# #         },
# #         json={ "text": text }
# #     )

# #     if response.status_code != 200:
# #         print("⚠️ Error: Deepgram TTS Error:", response.text)
# #         return

# #     with open(RESPONSE_MP3, 'wb') as f:
# #         f.write(response.content)
# #     print("🔊 Playing response...")
# #     playsound(RESPONSE_MP3)



# 🔊 Step 3: TTS with Deepgram SDK
def speak_response(text):
    try:
        print("🔊 Speaking (with SDK)...")

        # Initialize Deepgram client
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        # Set TTS options
        options = SpeakOptions(
            model="aura-asteria-en"
        )

        # Save the TTS audio to file
        response = deepgram.speak.v("1").save(RESPONSE_MP3, {"text": text}, options)

        print("🔊 Playing response...")
        playsound(RESPONSE_MP3)

    except Exception as e:
        print(f"⚠️ Error using Deepgram SDK: {e}")

# 🤖 Step 4: Simple Agent Logic (you can replace this with RAG later)
def agent(text):
    if "pda" in text.lower():
        return "PDAs are Program Derived Addresses used in Solana programs."
    elif "anchor" in text.lower():
        return "Anchor is a framework for Solana smart contract development."
    else:
        return "I'm not sure about that. Try asking about PDAs or Anchor."

# 🌀 Main Loop
def main():
    while True:
        record_audio(FILENAME)
        user_input = transcribe_audio(FILENAME)
        response = agent(user_input)
        speak_response(response)

if __name__ == "__main__":
    main()
