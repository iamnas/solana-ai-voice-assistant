import os
import json
from openai import OpenAI

class GptAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL_NAME", "gpt-4")  # default to gpt-4
        self.client = OpenAI(api_key=self.api_key)

    def get_response(self, text):
        prompt = (
            "You are a Solana voice assistant. Respond briefly in 1-2 sentences. "
            "If the user wants to end the conversation (e.g., says 'bye', 'stop', 'exit', 'thank you'), "
            "respond with a short goodbye message and return JSON: {\"reply\": <response>, \"end\": true}. "
            "Otherwise, return JSON: {\"reply\": <response>, \"end\": false}.\n\n"
            f"User: {text}\n"
            "Respond in JSON format only."
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You're a Solana expert voice assistant. Answer briefly in JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            content = response.choices[0].message.content.strip()
            print("🧠 Raw agent response:", content)

            # Try parsing the response as JSON
            data = json.loads(content)
            return data.get("reply", "Sorry, I couldn't understand."), data.get("end", False)

        except json.JSONDecodeError:
            return "Sorry, I couldn't parse the response.", False
        except Exception as e:
            return f"Error: {e}", True  # Safely end on error

