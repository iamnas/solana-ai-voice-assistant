import os
import json
import google.generativeai as genai
import re


class GoogleAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(os.getenv("GOOGLE_MODEL_NAME"))

    def get_response(self, text):
        prompt = (
            "You are a Solana voice assistant. Respond briefly in 1-2 sentences. "
            "If the user wants to end the conversation (e.g., says 'bye', 'stop', 'exit', 'thank you'), "
            "respond with a short goodbye and return JSON: {\"reply\": <response>, \"end\": true}. "
            "Otherwise, return JSON: {\"reply\": <response>, \"end\": false}.\n\n"
            f"User: {text}\n"
            "Respond in JSON format only."
        )

        try:
            response = self.model.generate_content(prompt)
            # content = response.text.strip()
            raw = response.text.strip()
            print("🧠 Raw agent response:", raw)

          # Strip ```json and ``` if present
            cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.MULTILINE).strip()
            data = json.loads(cleaned)

            return data.get("reply", "Sorry, I couldn't understand."), data.get("end", False)

        except json.JSONDecodeError as e:
            print("⚠️ JSON decode error:", e)
            return "Sorry, I couldn't parse the response.", False
        except Exception as e:
            return f"Error: {e}", True