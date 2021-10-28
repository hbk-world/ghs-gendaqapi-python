from .ghsapi_states import GHSReturnValue, returnKey
import socket
import errno
from . import jsonrpc
from struct import pack, unpack

MAX_CONNECTIONS = 30


class ConnectionHandler:

    connectionNumber = 0
    api_version_header = 1195638785

    def __init__(self):
        self.requestId = 0
        self.sock = 0
        self.ipAddress = 0

    def getNumOfConnections(self):
        return self.connectionNumber

    def getIpAddress(self):
        return self.ipAddress

    def ConnectionEstablish(self, ipAdress, portNum):
        self.ipAddress = ipAdress
        if self.getNumOfConnections() > MAX_CONNECTIONS:
            return GHSReturnValue["ConnectionFailed"]
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            return GHSReturnValue["ConnectionFailed"]
        try:
            self.sock.connect((ipAdress, portNum))
        except socket.gaierror as e:
            return GHSReturnValue["ConnectionFailed"]
        except ConnectionRefusedError:
            return GHSReturnValue["NoConnection"]
        self.connectionNumber += 1
        return GHSReturnValue["OK"]

    def SendRequestAndWaitResponse(self, methodName, methodParam):
        self.requestId += 1
        requestJSON = jsonrpc.createJSONrpc(self.requestId, methodName, methodParam)
        writeLen = len(requestJSON)
        headerSx = pack("!I", writeLen) + pack("!I", self.api_version_header)
        try:
            self.ConnectionWrite(headerSx, len(headerSx))
            self.ConnectionWrite(requestJSON, writeLen)
        except:
            return {returnKey: GHSReturnValue["NoConnection"]}

        # self.ConnectionWrite(headerSx, len(headerSx))
        # self.ConnectionWrite(requestJSON, writeLen)

        headerRxSize = 8
        headerRx = self.ConnectionRead(headerRxSize)
        if headerRxSize != len(headerRx):
            return {returnKey: GHSReturnValue["NOK"]}

        headerRxPacketHeader = unpack(">II", headerRx)
        if headerRxPacketHeader[1] != self.api_version_header:
            return {returnKey: GHSReturnValue["NOK"]}

        responseJSON = self.ConnectionRead(headerRxPacketHeader[0])
        return jsonrpc.parseJSONrpc(self.requestId, responseJSON)

    def ConnectionRead(self, length):
        message = b""
        while len(message) < length:
            try:
                packet = self.sock.recv(length - len(message))
                if not packet:
                    return None
                message += packet
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    print("No data available")
        return message

    def ConnectionWrite(self, message, length):
        totalsentBytes = 0
        sentBytes = 0
        while totalsentBytes < length:
            try:
                sentBytes = self.sock.send(message[totalsentBytes:])
            except socket.gaierror as e:
                raise OSError("Socket not Connected")
            if sentBytes == 0:
                raise RuntimeError("Socket Connection Broken")
            totalsentBytes = totalsentBytes + sentBytes
