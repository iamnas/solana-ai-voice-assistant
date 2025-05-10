# actions/get_balance.py

import random
from solana.rpc.api import Client
from solana.rpc.api import Pubkey
BALANCE_MESSAGES = [
    "You’ve got {sol:.4f} SOL — rich by crypto winter standards!",
    "Counting coins... That’s {sol:.4f} SOL. Flex responsibly.",
    "{sol:.4f} SOL? HODL or spend it on NFTs — your call.",
    "Wallet check: {sol:.4f} SOL. Probably more than your friend.",
    "Only {sol:.4f} SOL? Time to start shilling."
]

def run(address: str):
    client = Client("https://api.mainnet-beta.solana.com")

    if not address:
        return "No address? That’s like asking the price of oxygen."
    try:
        pubkey = Pubkey.from_string(address)
        response = client.get_balance(pubkey)
        lamports = response.value
        sol = lamports / 1_000_000_000
        message = random.choice(BALANCE_MESSAGES).format(sol=sol)
        return message
    except Exception as e:
        return f"Oops. Couldn't check your wallet — blame Solana RPC: {e}"
