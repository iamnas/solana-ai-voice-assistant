from deepgram import DeepgramClient, SpeakOptions
from playsound import playsound
import os
from dotenv import load_dotenv

load_dotenv()

# Config
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Your Deepgram API key
# DEEPGRAM_API_KEY = "your_actual_deepgram_key_here"

# Output filename
FILENAME = "output.mp3"

# The text to be spoken
TEXT = {
    "text": "Hello! This is a test of Deepgram's TTS using the Python SDK."
}


def speak_with_deepgram():
    try:
        print("🧠 Initializing Deepgram client...")
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        # Define TTS options
        options = SpeakOptions(
            model="aura-asteria-en",  # Other models: aura-orion-en, etc.
        )

        print("🔊 Requesting TTS from Deepgram...")
        # Save the TTS result to a file
        # response = deepgram.speak.v("1").save(FILENAME, TEXT, options)
        response = deepgram.speak.rest.v("1").save(FILENAME, TEXT, options)


        print("✅ TTS audio saved to:", FILENAME)

        print("▶️ Playing the audio...")
        playsound(FILENAME)

    except Exception as e:
        print(f"⚠️ Exception: {e}")


if __name__ == "__main__":
    speak_with_deepgram()
