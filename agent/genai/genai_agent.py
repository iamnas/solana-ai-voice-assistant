

import os
import json
import re
import google.generativeai as genai

from actions.get_balance import run as get_balance
from actions.get_solana_price import run as get_sol_price
from actions.get_token_price import run as get_token_price

class GoogleAgent:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(os.getenv("GOOGLE_MODEL_NAME"))

    def get_response(self, text):
        prompt = (
            "You are a Solana voice assistant. Respond briefly in 1-2 sentences.\n"
            "If the user wants to end the conversation (says 'bye', 'stop', 'exit', 'thank you'), "
            "respond with JSON: {\"reply\": <response>, \"end\": true}.\n"
            "If the user asks for their balance, include an action: \"get_balance\" and \"address\".\n"
            "If they ask for SOL price, set \"action\": \"get_sol_price\".\n"
            "If they ask for a token price, set \"action\": \"get_token_price\" and include \"token_address\".\n"
            "Otherwise, just reply normally in JSON: {\"reply\": ..., \"end\": false}.\n\n"
            f"User: {text}\n"
            "Respond in JSON format only."
        )

        try:
            response = self.model.generate_content(prompt)
            raw = response.text.strip()
            print("🧠 Raw agent response:", raw)

            # Remove markdown formatting if present
            cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.MULTILINE).strip()
            data = json.loads(cleaned)

            reply = data.get("reply", "Sorry, I couldn't understand.")
            end = data.get("end", False)
            action = data.get("action", None)

            # Optional actions
            if action == "get_balance" and "address" in data:
                reply = get_balance(data["address"])
            elif action == "get_sol_price":
                reply = get_sol_price()
            elif action == "get_token_price" and "token_address" in data:
                reply = get_token_price(data["token_address"])

            return reply, end, action

        except json.JSONDecodeError as e:
            print("⚠️ JSON decode error:", e)
            return "Sorry, I couldn't parse the response.", False
        except Exception as e:
            return f"Error: {e}", True
