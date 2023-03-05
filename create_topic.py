
import os
import asyncio


from dotenv import load_dotenv

load_dotenv()

from pkg.pubsub import dapp_create_topic_request


PUSH_DAPP_ID = os.getenv("PUSH_DAPP_ID")


async def main():

    topic_name = ""

    result = await dapp_create_topic_request(PUSH_DAPP_ID, topic_name)
    print("Create topic response: ", result)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

