import random
import requests

TOKEN_MESSAGES = [
    "Your token’s living its best life at ${price:.4f}.",
    "Current price: ${price:.4f}. Not bad, not rug (yet).",
    "Looks like ${price:.4f}. Could be meme, could be moon.",
    "Token price: ${price:.4f}. Better than 0, right?",
    "Selling for ${price:.4f}. You in or nah?"
]

def run(token_address: str):
    if not token_address:
        return "No token address? That’s like asking the price of oxygen."

    url = f"https://lite-api.jup.ag/price/v2?ids={token_address}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        price_data = data["data"].get(token_address)
        if price_data:
            price = float(price_data["price"])
            return random.choice(TOKEN_MESSAGES).format(price=price)
        else:
            return "No price found — maybe that token’s imaginary?"
    except Exception as e:
        return f"Couldn’t fetch token price. Tech gods said no: {e}"
