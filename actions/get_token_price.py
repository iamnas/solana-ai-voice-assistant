import requests

def run(token_address: str):
    url = f"https://lite-api.jup.ag/price/v2?ids={token_address}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        price_data = data["data"].get(token_address)
        if price_data:
            price = float(price_data["price"])
            return f"The token price is ${price:.4f}."
        else:
            return "Could not find token price. Please check the address."
    except Exception as e:
        return f"Failed to fetch token price: {e}"
