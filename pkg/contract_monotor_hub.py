from asyncio import wait_for, run, Queue
import ujson
from contract_monitors import CONTRACT_PARSERS


from config import WSS_RPC_URI
from websockets import connect


async def contract_monitor(queue: Queue):
    async with connect(WSS_RPC_URI) as ws:

        for cp in CONTRACT_PARSERS.keys():

            await ws.send(
                ujson.dumps(
                    {"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": [
                        "logs",
                        {
                            "address": cp,
                        }
                    ]
                    }
                )
            )

            subscription_response = await ws.recv()
            print(subscription_response)

        while True:
            # message = await wait_for(ws.recv(), timeout=600)
            message = await ws.recv()

            payload = ujson.loads(message)
            contract_addr = payload["params"]["result"]["address"]
            contract_parser = CONTRACT_PARSERS[contract_addr]
            try:
                data: dict = contract_parser(payload)
                # print(msg)
                await queue.put(data)
            except Exception as e:
                print(e)

if __name__ == "__main__":
    run(contract_monitor())
