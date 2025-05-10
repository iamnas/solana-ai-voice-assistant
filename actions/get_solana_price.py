import random
import requests

PRICE_MESSAGES = [
    "SOL is at ${price:.2f}. Time to moon or what?",
    "Latest SOL price: ${price:.2f}. Not financial advice, but still.",
    "You asked, I delivered: ${price:.2f} per SOL. Respect the drip.",
    "SOL = ${price:.2f}. Could be worse, could be FTT.",
    "One SOL goes for ${price:.2f}. Buy high, sell low!"
]

def run():
    url = "https://lite-api.jup.ag/price/v2?ids=So11111111111111111111111111111111111111112"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        price = float(data["data"]["So11111111111111111111111111111111111111112"]["price"])
        return random.choice(PRICE_MESSAGES).format(price=price)
    except Exception as e:
        return f"Couldn't grab SOL price. API ghosted us: {e}"
