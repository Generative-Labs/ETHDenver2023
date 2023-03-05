
import asyncio
import os

from dotenv import load_dotenv

load_dotenv()

from pkg.pubsub import dapp_subscribe_topic_request


SUBSCRIBE_DAPP_ID = os.getenv("SUBSCRIBE_DAPP_ID")
TOPIC_ID = os.getenv("TOPIC_ID")


async def main():


    result = await dapp_subscribe_topic_request(SUBSCRIBE_DAPP_ID, TOPIC_ID)
    print("Subscribe topic response: ", result)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

