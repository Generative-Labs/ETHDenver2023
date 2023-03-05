from config import W3
from eth_abi import decode_single

ABI = '[{"inputs":[{"internalType":"address","name":"_logic","type":"address"},{"internalType":"address","name":"admin_","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"beacon","type":"address"}],"name":"BeaconUpgraded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"admin_","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"implementation_","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"stateMutability":"payable","type":"receive"}]'

tBTC_CONTRACT_ADDR = "0xdac17f958d2ee523a2206206994597c13d831ec7"

CONTRACT = W3.eth.contract(
    address=W3.toChecksumAddress(tBTC_CONTRACT_ADDR), abi=ABI)


tBTC_CONTRACT_PARAMETERS = {
    "address": tBTC_CONTRACT_ADDR,
    "topics": ["0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925"],
}


def tBTC_Parser(payload: dict) -> dict:
    value = decode_single(
        "(uint256)",
        bytearray.fromhex(
            payload["params"]["result"]["data"][2:]),
    )[0]
    # print(value)
    from_user = payload["params"]["result"]["topics"][1][26:]
    to_user = payload["params"]["result"]["topics"][2][26:]
    msg = f"User 0x{from_user} transfer {value} to 0x{to_user}, TransactionHash:{payload['params']['result']['transactionHash']}"
    # print(msg)
    return {
        "title": "Transfer event",
        "content": msg,
    }
