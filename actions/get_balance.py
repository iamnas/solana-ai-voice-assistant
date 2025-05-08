# # actions/get_balance.py

# from solana.rpc.api import Client
# from solana.rpc.api import Pubkey

# def run():
#     address = input("🔐 Please type your Solana address: ").strip()
    
#     client = Client("https://api.mainnet-beta.solana.com")

#     try:
#         pubkey = Pubkey.from_string(address)
#         response = client.get_balance(pubkey)
#         lamports = response.value
#         sol = lamports / 1_000_000_000
#         return f"Your balance is {sol:.4f} SOL."
#     except Exception as e:
#         return f"Failed to fetch balance: {e}"


# actions/get_balance.py

from solana.rpc.api import Client
from solana.rpc.api import Pubkey

def run(address: str):
    client = Client("https://api.mainnet-beta.solana.com")

    try:
        pubkey = Pubkey.from_string(address)
        response = client.get_balance(pubkey)
        lamports = response.value
        sol = lamports / 1_000_000_000
        return f"Your balance is {sol:.4f} SOL."
    except Exception as e:
        return f"Failed to fetch balance: {e}"
