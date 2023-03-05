import time
import asyncio


from .message_pb2 import Web3MQMessageListResponse, Web3MQCommonMessage
from .connect_pb2 import DAppConnectResp, DAppConnectCommand

from .pbtype import PbTypeNotificationListResp, DAppCategoryByte, PbTypeDAppConnectReq, PbTypeDAppConnectResp, PbTypeMessage


async def send_dapp_connect(ws, dappid):
    cmd = DAppConnectCommand()

    nodeid = "nodeid"
    cmd.DAppID = dappid
    cmd.NodeID = nodeid
    cmd.Timestamp = int(time.time() * 1000)

    bytelist = bytearray([DAppCategoryByte, PbTypeDAppConnectReq])

    bytelist.extend(cmd.SerializeToString())

    await ws.send(bytelist)


class Web3MQException(Exception):
    pass


def parse_response(bytedata):
    if len(bytedata) < 3:
        raise Web3MQException("Invalid byte data")

    category, pb_type = bytedata[0], bytedata[1]
    if category != DAppCategoryByte:
        raise Web3MQException("Invalid Category Type")

    if pb_type == PbTypeNotificationListResp:
        return pb_type, Web3MQMessageListResponse.FromString(bytedata[2:])
    if pb_type == PbTypeDAppConnectResp:
        return pb_type, DAppConnectResp.FromString(bytedata[2:])
    if pb_type == PbTypeMessage:
        return pb_type, Web3MQCommonMessage.FromString(bytedata[2:])

    raise Web3MQException("Unsupported Protobuf Type")
