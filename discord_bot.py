import os
import asyncio

from ujson import loads

import discord
import websockets
from discord.ext import commands

from dotenv import load_dotenv

from pkg.web3mq_client import send_dapp_connect, parse_response
from pkg.pbtype import PbTypeDAppConnectResp, PbTypeMessage, PbTypeNotificationListResp

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

WEB3MQ_WEBSOCKET_ADDRESS = os.getenv('WEB3MQ_WEBSOCKET_ADDRESS')

SUBSCRIBE_DAPP_ID = os.getenv("SUBSCRIBE_DAPP_ID")

DiscordChan = None


def get_embed():
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.add_field(name="Field1", value="hi", inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)
    return embedVar


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        global DiscordChan

        DiscordChan = self.get_channel(int(DISCORD_CHANNEL_ID))

        print(DiscordChan)

        await DiscordChan.send("Hello Bot Online")
        # await DiscordChan.send(embed=get_embed())

    async def on_message(self, message):
        print(">>>>", message)
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


async def bot_message_handler(msgobj):
    result = msgobj.payload.decode()
    # print(result)

    if msgobj.payloadType.startswith("application/json"):
        json_data = loads(result)
        msgdata = json_data["title"]
    else:
        msgdata = result

    if DiscordChan:
        await DiscordChan.send(msgdata)
        # Send a simple text message or your can use embed message


        # embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
        # embedVar.add_field(name="Field1", value="hi", inline=False)
        # await DiscordChan.send(embed=embedVar)


async def handler_web3mq_message(message):
    pbtype, respobj = parse_response(message)
    # print(">>>", pbtype, ' ', respobj)

    if pbtype == PbTypeDAppConnectResp:
        print(respobj.StatusCode)
        print(respobj.StatusMsg)

    if pbtype == PbTypeMessage:
        await bot_message_handler(respobj)

    if pbtype == PbTypeNotificationListResp:
        # print(respobj)
        for item in respobj.data:
            await bot_message_handler(item)


async def web3mq_loop_handler():
    await client.wait_until_ready()

    connection = websockets.connect(uri=WEB3MQ_WEBSOCKET_ADDRESS)

    # The client is also as an asynchronous context manager.
    async with connection as websocket:
        try:
            # Init dapp <-> web3mq connection
            await send_dapp_connect(websocket, SUBSCRIBE_DAPP_ID)
            resp = await websocket.recv()
            await handler_web3mq_message(resp)

            # Receives the replies.
            async for message in websocket:
                # print(message)
                await handler_web3mq_message(message)
        except Exception as err:
            print(err)


async def discord_bot_handler():
    print("bot online")
    await client.start(DISCORD_TOKEN)


async def main():
    task1 = asyncio.create_task(discord_bot_handler())
    task2 = asyncio.create_task(web3mq_loop_handler())

    try:
        await asyncio.wait([task1, task2])
    except KeyboardInterrupt:
        task1.cancel()
        task2.cancel()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
