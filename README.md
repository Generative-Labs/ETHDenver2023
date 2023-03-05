# Web3MQ DApp discord demo

> There are 2 web3mq environments could be used for this demo app.

`You should connect to same network, devnet or testnet`

`web3mq endpoints of devnet`

- wss://dev-us-west-2.web3mq.com/messages
- wss://dev-ap-singapore-1.web3mq.com/messages
- wss://dev-ap-jp-1.web3mq.com/messages

`web3mq endpoints of testnet`

- wss://testnet-ap-singapore-1.web3mq.com/messages
- wss://testnet-ap-jp-1.web3mq.com/messages
- wss://testnet-ap-singapore-2.web3mq.com/messages
- wss://testnet-ap-jp-2.web3mq.com/messages
- wss://testnet-us-west-1-2.web3mq.com/messages
- wss://testnet-us-west-1-1.web3mq.com/messages

## Steps

- 1. Create two dapps (push dapp and subscribe dapp)
- 2. Push DApp create topic; Configuring .env file and execute `python create_topic.py`
- 3. Subscribe DApp subscribe previous topic; Configuring .env file and execute `python subscribe_topic.py`
- 4. Create discord bot, get discord token and channel id;
    - See more detail about discord bot https://forwardforever.com/how-to-create-discord-bot-with-power-automate/;
- 5. Configuring subscribe dapp .env file and execute `python discord_bot.py`
- 6. Configuring push dapp .env file and execute `python eth_scan.py`


`Install python dependency`

```bash
# If your Python version is greater than or equal to 3.10,
# You will need to upgrade your Websockets version as soon as you have finished installing the project 
# dependencies, you may encounter a dependency conflict due to the low version of Websockets 
# that Web.py depends on, please ignore it.

pip install -r requirements.txt
```

### 1. Create two dapps

- Generate a ed25519 keypair
- Use ed25519 pubkey as dapp pubkey
- [Create DApp Page] choose the same environment (testnet or devnet)
    - [testnet page](https://pushmq-backstage.pages.dev/)
    - [devnet page](https://dev.pushmq-backstage.pages.dev/)


<!-- - [Create DApp](https://docs.web3mq.com/docs/Web3MQ-API/dapp/create_dapp)
- [DApp Create Topic docs](https://docs.web3mq.com/docs/Web3MQ-API/dapp/dapp_create_topic)
- [DApp Subscribe Topic docs](https://docs.web3mq.com/docs/Web3MQ-API/dapp/dapp_subscribe_topic)
 -->

> One dapp create a topic, another subscribe this topic

> `Two dapps should connect to same network. devnet or testnet`

### 2. Push DApp Create topic

Configuring your .env file

```bash
# web3mq api address
WEB3MQ_API_ADDRESS = "https://dev-ap-singapore-1.web3mq.com"
PUSH_DAPP_ID = "<your push dapp_id>"/
PUSH_DAPP_PRIVATE_KEY = "<your push dapp private key>"
```

`Create topic`

```bash
python create_topic.py
```

> Configuring .env file `TOPIC_ID` field after execute create_topic.py

```bash
TOPIC_ID = "<your topic id after execute create_topic.py>"
```

### 3. Subscribe DApp subscribe previous topic

> Configuring .env file and execute `python subscribe_topic.py`

```bash
# web3mq api address
WEB3MQ_API_ADDRESS = "https://dev-ap-singapore-1.web3mq.com"
SUBSCRIBE_DAPP_ID = "<your push dapp_id>"/
SUBSCRIBE_DAPP_PRIVATE_KEY = "<your push dapp private key>"

TOPIC_ID = "<previous topic id after execute create_topic.py>"
```

`Susbscribe topic`

```bash
python subscribe_topic.py
```


### 4. Create discord bot

https://discord.com/developers/docs/intro

- 1. Login discord website
- 2. Go to https://discord.com/developers/applications
    - Click New Application button and create a bot
- 3. Go to Bot menu and click `Add Bot` button
- 4. Copy your `TOKEN` and configuring .env file in next steps
- 5. Click `OAuth2` menu, and click `bot` in scopes area
- 6. Select `Send Messages` or more BOT PERMISISONS if your need
- 7. Copy authorization url link and confirm 

More detail about create discord bot, you can visit
https://forwardforever.com/how-to-create-discord-bot-with-power-automate/

or discord website

### 5. Subscribe client steps

Configuring your .env file

```bash
DISCORD_TOKEN = "<your discord token>"
DISCORD_CHANNEL_ID = "<your channel id>"

# web3mq websocket address

WEB3MQ_WEBSOCKET_ADDRESS = "wss://dev-ap-singapore-1.web3mq.com/messages"

SUBSCRIBE_DAPP_ID = "<your subscribe dapp_id>"

SUBSCRIBE_DAPP_PRIVATE_KEY = "<your subscribe dapp private key>"
```

```bash
python discord_bot.py
```


### 6. Publish client steps

Configuring your .env file

```bash
# web3mq api address

ETH_WEBSOCKET_URI = "<your eth subscribe websocket rpc>"

WEB3MQ_API_ADDRESS = "https://dev-ap-singapore-1.web3mq.com"

PUSH_DAPP_ID = "<your dapp id>"

TOPIC_ID = "<your topic id>"

PUSH_DAPP_PRIVATE_KEY = "<your push dapp private key>"

INFURA_APIKEY = "<your infura key>, you can get one for free at https://infura.io"
```

```bash
python eth_scan.py
```


## How to add your contract monitor?

In the "contract_monitors" directory, we have created a number of contract monitors,

you can make a copy of a contract monitor, such as USDT_copy.py, and rename the file to your contract name as you wish,

change the "XXXX_CONTRACT_ADDR" of source file to your contract address, change the "XXXX_Parser" to your contract data parser.

Finally, you need to import your contract address and parser into the CONTRACT_PARSERS variable in the *\_\_init__.py* file.