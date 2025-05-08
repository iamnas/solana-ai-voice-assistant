import os
import json
from openai import OpenAI

from actions import handle_intent

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
            },
            {
                "type": "function",
                "function": {
                    "name": "get_solana_price",
                    "description": "Gets the current market price of SOL.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_token_price",
                    "description": "Gets the current market price of a token by address.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_address": {
                                "type": "string",
                                "description": "The SPL token address to fetch price for."
                            }
                        },
                        "required": ["token_address"]
                    }
                }
            }
        ]

    def get_response(self, text):
        prompt = (
            "You are a Solana voice assistant. Respond briefly in 1-2 sentences.\n"
            "Also, include a machine-readable `intent` field to guide actions (e.g., 'get_balance','get_token_price', 'get_solana_price', 'none').\n"
            "If the user wants to end the conversation (e.g., 'bye', 'stop', etc.), reply shortly and return: `end: true`, intent: 'end'.\n\n"
            f"User: {text}\n"
            "Respond ONLY in JSON like this:\n"
            "{\"reply\": <response>, \"end\": <true|false>, \"intent\": <string>}"
        )

        try:
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

            tool_calls = response.choices[0].message.tool_calls
            content = response.choices[0].message.content

            if tool_calls:
                print("🔧 Tool call detected:", tool_calls)
                tool = tool_calls[0].function
                tool_name = tool.name
                tool_args = json.loads(tool.arguments)

                # Call your handler function
                result = handle_intent(tool_name, **tool_args)
                return result, False, tool_name

            # No tool call, fallback to natural response
            print("🧠 Raw agent response:", content)
            data = json.loads(content)
            return data.get("reply", "Sorry, I couldn't understand."), data.get("end", False), data.get("intent", "none")

        except json.JSONDecodeError:
            return "Sorry, I couldn't parse the response.", False, "none"
        except Exception as e:
            return f"Error: {e}", True, "none"

    # def get_response(self, text):
    #     prompt = (
    #         "You are a Solana voice assistant. Respond briefly in 1-2 sentences.\n"
    #         "Also, include a machine-readable `intent` field to guide actions (e.g., 'get_balance','get_token_price', 'get_solana_price', 'none').\n"
    #         "If the user wants to end the conversation (e.g., 'bye', 'stop', etc.), reply shortly and return: `end: true`, intent: 'end'.\n\n"
    #         f"User: {text}\n"
    #         "Respond ONLY in JSON like this:\n"
    #         "{\"reply\": <response>, \"end\": <true|false>, \"intent\": <string>}"
    #     )

    #     try:
    #         # ✨ Using tool calling
    #         response = self.client.chat.completions.create(
    #             model=self.model,
    #             messages=[
    #                 {"role": "system", "content": "You're a Solana expert voice assistant. Return response, end, and intent in JSON."},
    #                 {"role": "user", "content": prompt}
    #             ],
    #             tools=self.tools,
    #             tool_choice="auto",
    #             max_tokens=150
    #         )

    #         content = response.choices[0].message.content
    #         tool_call = response.choices[0].message.tool_calls

    #         if tool_call:
    #             print("🔧 Tool call detected:", tool_call)
    #             # You can handle tool execution logic here if needed
    #             # For now we just fallback to basic intent system

    #         # 🧠 Parse the JSON response from assistant
    #         print("🧠 Raw agent response:", content)
    #         data = json.loads(content)

    #         return data.get("reply", "Sorry, I couldn't understand."), data.get("end", False), data.get("intent", "none")

    #     except json.JSONDecodeError:
    #         return "Sorry, I couldn't parse the response.", False, "none"
    #     except Exception as e:
    #         return f"Error: {e}", True, "none"
