# 🎙️ Solana AI Voice Assistant

A Python-based voice assistant that uses Whisper for speech-to-text (STT), a simple agent for response generation, and Deepgram for text-to-speech (TTS) — tailored for Solana devs.

## 🔧 Features

- 🎤 Record audio via microphone
- 📝 Transcribe speech using [OpenAI Whisper](https://github.com/openai/whisper)
- 🤖 Respond using a simple rules-based agent (customizable for Solana questions)
- 🔊 Speak responses using [Deepgram TTS](https://developers.deepgram.com/docs/tts/)
- 🔁 Continuous interaction loop

## 🛠 Requirements

- Python 3.10+
- Conda (recommended)
- A Deepgram API key ([get one here](https://console.deepgram.com/signup))

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/your-username/solana-ai-voice-assistant.git
cd solana-ai-voice-assistant

# Create environment
conda create -n solana-voice python=3.10 -y
conda activate solana-voice

# Install dependencies
pip install -r requirements.txt
````

## 🧪 Run the App

```bash
# Add your Deepgram API key to .env
echo "DEEPGRAM_API_KEY=your_api_key_here" > .env

# Run the assistant
python main.py
```

## 📁 File Structure

```
voice-agent/
├── .env                         # Environment variables (e.g., API keys)
├── README.md                    # Project overview and setup instructions
├── requirements.txt             # Python dependencies
├── main.py                      # Main voice assistant loop (record, transcribe, respond, speak)
├── agent/                       # Agent framework
│   ├── __init__.py
│   ├── agent.py                 # Central loader to select active agent
│   ├── openai_agent/
│   │   └── gpt_agent.py         # Uses OpenAI GPT (e.g., GPT-4)
│   ├── local_agent/
│   │   └── local_llm.py         # Talks to local LLMs (e.g., via Ollama)
│   ├── rag_agent/
│   │   ├── __init__.py
│   │   └── rag.py               # Retrieval-augmented generation logic
│   └── genai_agent/
│       └── genai_agent.py       # Custom GenAI agent implementation
│
│
├── actions/
|_____                       

```

## 🧠 Example Q\&A

You can ask the assistant things like:

* “What is a PDA in Solana?”
* “Tell me about Anchor framework.”
* “Explain CPI calls.”

## 🗣 Tech Stack

* Whisper (STT)
* Deepgram SDK (TTS)
* Python (with SoundDevice, NumPy, Playsound, etc.)

## 🚀 Future Ideas

* Replace the rules-based agent with a Retrieval-Augmented Generation (RAG) model
* Add live VAD-based continuous listening
* Integrate with Solana CLI or on-chain contract interactions
