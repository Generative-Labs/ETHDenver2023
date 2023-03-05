import os
import httpx
import time

from .signature import ed25519_sign_data_base64



from dotenv import load_dotenv

load_dotenv()


WEB3MQ_API_ADDRESS = os.getenv("WEB3MQ_API_ADDRESS")

PUSH_DAPP_PRIVATE_KEY = os.getenv("PUSH_DAPP_PRIVATE_KEY")

SUBSCRIBE_DAPP_PRIVATE_KEY = os.getenv("SUBSCRIBE_DAPP_PRIVATE_KEY")




async def dapp_publish_topic_message(dapp_id, topicid, title, content):
    timestamp = int(time.time() * 1000)

    signature_content = dapp_id + topicid  + str(timestamp)

    signature = ed25519_sign_data_base64(PUSH_DAPP_PRIVATE_KEY, signature_content)

    data = {
        "dapp_id": dapp_id,
        "topicid": topicid,
        "title": title,
        "content": content,
        "timestamp": timestamp,
        "web3mq_dapp_signature": signature,
    }


    # print(data)
    async with httpx.AsyncClient() as client:
        response = await client.post(WEB3MQ_API_ADDRESS + "/api/dapp_publish_topic_message/", json=data)

        return response.json()



async def _dapp_create_topic(dapp_id, topic_name, timestamp, signature):
    data = {
        "dapp_id": dapp_id,
        "topic_name": topic_name,

        "timestamp": timestamp,
        "web3mq_dapp_signature": signature,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(WEB3MQ_API_ADDRESS + "/api/dapp_create_topic/", json=data)

        return response.json()



async def dapp_create_topic_request(dapp_id, topic_name=""):
    timestamp = int(time.time() * 1000)


    signature_content = dapp_id + str(timestamp)

    signature = ed25519_sign_data_base64(PUSH_DAPP_PRIVATE_KEY, signature_content)

    result = await _dapp_create_topic(dapp_id, topic_name, timestamp, signature)


    return result


    # {
    #     "msg":"Ok",
    #     "code":0,
    #     "data":{
    #         "topic_name":"your topic name",
    #         "topicid":"topic:9aae3fa85c0ce5622bdfca41fc6f250d5c322555"
    #     }
    # }



async def _dapp_subscribe_topic(dapp_id, topicid, status, timestamp, signature):
    data = {
        "dapp_id": dapp_id,
        "topicid": topicid,
        "status": status,
        "timestamp": timestamp,
        "web3mq_dapp_signature": signature,
    }



    async with httpx.AsyncClient() as client:
        response = await client.post(WEB3MQ_API_ADDRESS + "/api/dapp_subscribe_topic/", json=data)

        return response.json()



async def dapp_subscribe_topic_request(dapp_id, topicid):
    timestamp = int(time.time() * 1000)

    status = 1  # 0 unsubscribe    1 subscribe
    signature_content = dapp_id + topicid  + str(status) + str(timestamp)

    signature = ed25519_sign_data_base64(SUBSCRIBE_DAPP_PRIVATE_KEY, signature_content)

    result = await _dapp_subscribe_topic(dapp_id, topicid, status, timestamp, signature)
    return result
