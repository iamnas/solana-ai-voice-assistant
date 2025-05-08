from actions.get_balance import handle_get_balance

INTENT_HANDLERS = {
    "get_balance": handle_get_balance,
    # "send_token": handle_send_token,
    # "get_price": handle_get_price,
    # Add more intents here
}

def handle_intent(intent: str, params: dict) -> str:
    handler = INTENT_HANDLERS.get(intent)
    if handler:
        return handler(params)
    return "Sorry, I don't know how to handle that request."
