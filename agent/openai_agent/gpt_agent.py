

# import os
# import json
# from openai import OpenAI

# class GptAgent:
#     def __init__(self):
#         self.tools = [
#             {
#                 "type": "function",
#                 "function": {
#                     "name": "get_balance",
#                     "description": "Gets the SOL balance of a given Solana wallet address.",
#                     "parameters": {
#                         "type": "object",
#                         "properties": {
#                             "address": {
#                                 "type": "string",
#                                 "description": "The Solana wallet address to check balance for."
#                             }
#                         },
#                         "required": ["address"]
#                     }
#                 }
#             }
#         ]

#         self.api_key = os.getenv("OPENAI_API_KEY")
#         self.model = os.getenv("MODEL_NAME", "gpt-4")
#         self.client = OpenAI(api_key=self.api_key)

#     def get_response(self, text):
#         prompt = (
#             "You are a Solana voice assistant. Respond briefly in 1-2 sentences.\n"
#             "Also, include a machine-readable `intent` field to guide actions (e.g., 'get_balance', 'get_price', 'none').\n"
#             "If the user wants to end the conversation (e.g., 'bye', 'stop', etc.), reply shortly and return: `end: true`, intent: 'end'.\n\n"
#             f"User: {text}\n"
#             "Respond ONLY in JSON like this:\n"
#             "{\"reply\": <response>, \"end\": <true|false>, \"intent\": <string>}"
#         )

#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": "You're a Solana expert voice assistant. Return response, end, and intent in JSON."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 tools=self.tools,
#                 tool_choice="auto",  # let model decide based on intent
#                 max_tokens=150
#             )
#             content = response.choices[0].message.content.strip()
#             print("🧠 Raw agent response:", content)

#             data = json.loads(content)
#             return data.get("reply", "Sorry, I couldn't understand."), data.get("end", False), data.get("intent", "none")

#         except json.JSONDecodeError:
#             return "Sorry, I couldn't parse the response.", False, "none"
#         except Exception as e:
#             return f"Error: {e}", True, "none"


import os
import json
from openai import OpenAI

class GptAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL_NAME", "gpt-4")
        self.client = OpenAI(api_key=self.api_key)

        # 🛠️ Tool (function) definitions
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_balance",
                    "description": "Gets the SOL balance of a given Solana wallet address.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "The Solana wallet address to check balance for."
                            }
                        },
                        "required": ["address"]
                    }
                }
            }
            # Add more tools/functions here in future
        ]

    def get_response(self, text):
        prompt = (
            "You are a Solana voice assistant. Respond briefly in 1-2 sentences.\n"
            "Also, include a machine-readable `intent` field to guide actions (e.g., 'get_balance', 'get_price', 'none').\n"
            "If the user wants to end the conversation (e.g., 'bye', 'stop', etc.), reply shortly and return: `end: true`, intent: 'end'.\n\n"
            f"User: {text}\n"
            "Respond ONLY in JSON like this:\n"
            "{\"reply\": <response>, \"end\": <true|false>, \"intent\": <string>}"
        )

        try:
            # ✨ Using tool calling
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You're a Solana expert voice assistant. Return response, end, and intent in JSON."},
                    {"role": "user", "content": prompt}
                ],
                tools=self.tools,
                tool_choice="auto",
                max_tokens=150
            )

            content = response.choices[0].message.content
            tool_call = response.choices[0].message.tool_calls

            if tool_call:
                print("🔧 Tool call detected:", tool_call)
                # You can handle tool execution logic here if needed
                # For now we just fallback to basic intent system

            # 🧠 Parse the JSON response from assistant
            print("🧠 Raw agent response:", content)
            data = json.loads(content)

            return data.get("reply", "Sorry, I couldn't understand."), data.get("end", False), data.get("intent", "none")

        except json.JSONDecodeError:
            return "Sorry, I couldn't parse the response.", False, "none"
        except Exception as e:
            return f"Error: {e}", True, "none"
