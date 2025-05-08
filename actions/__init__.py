# actions/__init__.py

from actions.get_balance import run as get_balance

intent_map = {
    "get_balance": get_balance,
    # Add more mappings here
}

def handle_intent(intent: str):
    handler = intent_map.get(intent)
    if handler:
        return handler()
    print(f"⚠️ Unknown intent: {intent}")
    return "Sorry, I don’t know how to handle that yet."
