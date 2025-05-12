import os
import json
import re
import google.generativeai as genai

from actions import handle_intent  # Same handler used for tool functions

class GoogleAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(os.getenv("GOOGLE_MODEL_NAME", "gemini-pro"))

        # 🛠️ Define available tool-like intents
        self.valid_intents = {
            "get_balance",
            "get_token_price",
            "get_solana_price",
            "end",
            "none"
        }

    def get_response(self, text):
        prompt = (
            "You're a laid-back, slightly sarcastic Solana voice assistant with a funny tone. "
            "Your job is to help with wallet balances, token prices, and Solana stuff, but do it with some sass. "
            "Respond briefly in 1–2 sentences max.\n\n"
            "Also include a machine-readable `intent` field to guide actions "
            "(e.g., 'get_balance', 'get_token_price', 'get_solana_price', 'none'). "
            "If the user wants to end the conversation (e.g., 'bye', 'stop', 'exit'), return: `end: true`, intent: 'end'.\n\n"
            f"User: {text}\n"
            "Respond ONLY in JSON format like this:\n"
            "{\"reply\": <response>, \"end\": <true|false>, \"intent\": <string>}"
        )

        try:
            response = self.model.generate_content(prompt)
            raw = response.text.strip()
            print("🧠 Raw agent response:", raw)

            # Clean code block formatting if present
            cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.MULTILINE).strip()
            data = json.loads(cleaned)

            reply = data.get("reply", "Sorry, I couldn't understand.")
            end = data.get("end", False)
            intent = data.get("intent", "none")

            if intent in self.valid_intents and intent != "none" and intent != "end":
                # Attempt to extract arguments if they exist
                args = data.get("args", {})  # Optional, extend your prompt if needed
                result = handle_intent(intent, **args)
                return result, False, intent

            return reply, end, intent

        except json.JSONDecodeError as e:
            print("⚠️ JSON decode error:", e)
            return "Sorry, I couldn't parse the response.", False, "none"
        except Exception as e:
            return f"Error: {e}", True, "none"
