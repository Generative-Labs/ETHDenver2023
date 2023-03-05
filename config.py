from web3 import Web3
from os import getenv

INFURA_APIKEY = getenv("INFURA_APIKEY")

if (len(INFURA_APIKEY) == 0) or (not INFURA_APIKEY):
    raise BaseException(
        "Undefined INFURA_APIKEY in .env file. You can get one for free by signing up at https://infura.io")


HTTPS_RPC_URI = f"https://mainnet.infura.io/v3/{INFURA_APIKEY}"
WSS_RPC_URI = f"wss://mainnet.infura.io/ws/v3/{INFURA_APIKEY}"


W3 = Web3(
    Web3.WebsocketProvider(WSS_RPC_URI)
)
