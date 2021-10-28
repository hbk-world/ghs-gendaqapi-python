from .connectionAPI import Connection
from .connection import ConnectionHandler

CLIENT_API_VERSION = 4


class GHS:
    def __init__(self):
        self._conHandle = ConnectionHandler()
        self._connection = Connection()

    ### Connection APIs ###
    def GHSConnect(self, ipAdress, portNum):
        return self._connection.Connect(
            self._conHandle, ipAdress, portNum, CLIENT_API_VERSION
        )

    def GHSDisconnect(self):
        return self._connection.Disconnect(self._conHandle)

    def GHSGetClientAPIVersion(self):
        return CLIENT_API_VERSION
