import asyncio
import os

from pkg.pubsub import dapp_publish_topic_message
from pkg.contract_monotor_hub import contract_monitor

from dotenv import load_dotenv

load_dotenv()


PUSH_DAPP_ID = os.getenv("PUSH_DAPP_ID")
TOPIC_ID = os.getenv("TOPIC_ID")


ETH_WEBSOCKET_URI = os.getenv('ETH_WEBSOCKET_URI')


async def web3mq_publish_handler(queue: asyncio.Queue):
    while True:
        data = await queue.get()

        title = data["title"]
        content = data["content"]

        # Limit sending frequency
        resp = await dapp_publish_topic_message(PUSH_DAPP_ID, TOPIC_ID, title, content)
        # print("DApp publish resp: ", resp)


async def main():
    queue = asyncio.Queue()

    task1 = asyncio.create_task(contract_monitor(queue))
    task2 = asyncio.create_task(web3mq_publish_handler(queue))

    try:
        await asyncio.wait([task1, task2])

        await queue.join()
    except KeyboardInterrupt:
        task1.cancel()
        task2.cancel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
