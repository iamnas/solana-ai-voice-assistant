from actions.get_balance import run as get_balance
from actions.get_solana_price import run as get_solana_price
from actions.get_token_price import run as get_token_price

intent_map = {
    "get_balance": get_balance,
    "get_solana_price": get_solana_price,
    "get_token_price": get_token_price,
}

def handle_intent(intent: str, data: str = None):
    handler = intent_map.get(intent)
    if handler:
        return handler(data) if data else handler()
    print(f"⚠️ Unknown intent: {intent}")
    return "Sorry, I don’t know how to handle that yet."
