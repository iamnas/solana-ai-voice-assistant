from solana.rpc.api import Pubkey
from solana.rpc.api import Client

public_key_string = "EnNgx1Dy9okKLV9QYZBpyFUpnCCvHYE8dGxvNoFZTvvQ"
public_key = Pubkey.from_string(public_key_string)
print(f"Public Key: {public_key}")



# # actions/get_balance.py

# from solana.rpc.api import Pubkey

# def run():
#     address = input("🔐 Please type your Solana address: ").strip()
    
client = Client("https://api.mainnet-beta.solana.com")


# pubkey = Pubkey.from_string(public_key)
response = client.get_balance(public_key)
print(response.value)
# lamports = response['result']['value']
# sol = lamports / 1_000_000_000
# print(f"Your balance is {sol:.4f} SOL.")