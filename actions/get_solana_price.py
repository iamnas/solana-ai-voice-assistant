import requests

def run():
    url = "https://lite-api.jup.ag/price/v2?ids=So11111111111111111111111111111111111111112"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        price = data["data"]["So11111111111111111111111111111111111111112"]["price"]
        return f"Current SOL price is ${float(price):.2f}."
    except Exception as e:
        return f"Failed to get SOL price: {e}"
