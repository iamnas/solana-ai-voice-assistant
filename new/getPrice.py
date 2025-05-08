# https://lite-api.jup.ag/price/v2?ids=JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN,So11111111111111111111111111111111111111112


# {
#   "data": {
#     "So11111111111111111111111111111111111111112": {
#       "id": "So11111111111111111111111111111111111111112",
#       "type": "derivedPrice",
#       "price": "160.215295500"
#     },
#     "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": {
#       "id": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
#       "type": "derivedPrice",
#       "price": "0.462691"
#     }
#   },
#   "timeTaken": 0.006070019
# }


# https://lite-api.jup.ag/price/v2?ids=Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB,So11111111111111111111111111111111111111112

# {
#   "data": {
#     "So11111111111111111111111111111111111111112": {
#       "id": "So11111111111111111111111111111111111111112",
#       "type": "derivedPrice",
#       "price": "159.770767000"
#     },
#     "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": {
#       "id": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
#       "type": "derivedPrice",
#       "price": "1.000075"
#     }
#   },
#   "timeTaken": 0.002369088
# }


# https://lite-api.jup.ag/price/v2?ids=he1iusmfkpAdwvxLNGV8Y1iSbj4rUy6yMhEA3fotn9A
# {
#   "data": {
#     "he1iusmfkpAdwvxLNGV8Y1iSbj4rUy6yMhEA3fotn9A": {
#       "id": "he1iusmfkpAdwvxLNGV8Y1iSbj4rUy6yMhEA3fotn9A",
#       "type": "derivedPrice",
#       "price": "174.280552478"
#     }
#   },
#   "timeTaken": 0.003893148
# }


# from solana.rpc.api import Pubkey
# from solana.rpc.api import Client

# from spl.token.instructions import get_associated_token_address

# def get_token_balance(wallet_address: str, token_mint: str):
#     client = Client("https://api.mainnet-beta.solana.com")
    
#     wallet_pubkey = Pubkey.from_string(wallet_address)
#     token_mint_pubkey = Pubkey.from_string(token_mint)

#     # Get associated token account (ATA) address
#     ata = get_associated_token_address(wallet_pubkey, token_mint_pubkey)
    

#     # Fetch token account info
#     resp = client.get_token_account_balance(ata)

#     print("res",resp.value)
#     if resp.value:
#         amount = resp.value.ui_amount_string
#         print(f"Token Balance: {amount}")
#         return amount
#     else:
#         print("No token account found.")
#         return "0"

# # Example usage
# get_token_balance("EnNgx1Dy9okKLV9QYZBpyFUpnCCvHYE8dGxvNoFZTvvQ", "he1iusmfkpAdwvxLNGV8Y1iSbj4rUy6yMhEA3fotn9A")

