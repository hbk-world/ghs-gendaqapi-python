"""GEN DAQ API - Python.

The GEN DAQ API can be used to control the HBM GEN Series tethered
mainframes without using Perception.

Package Contents:
    Connections: Connection related API functions
"""

from .connection import ConnectionHandler
from . import connection_api as _connection
from .ghsapi_states import RETURN_KEY, GHSReturnValue

CLIENT_API_VERSION = 4


class GHS:
    """GEN DAQ API object.

    Attributes:
        _con_handle: An unique identifier per mainframe connection.
    """

    def __init__(self):
        self._con_handle = ConnectionHandler()

    # Connection related API functions
    def ghs_connect(self, ip_address, port_num):
        """Establishes a connection to the mainframe.

        Args:
            ip_address: IP address needs to be an IPV4 address.
                "localhost" is also supported.
            port_num: TCP port number (currently defined as 8006).

        Returns:
            String value representing API status.
        """

        return _connection.connect(
            self._con_handle, ip_address, port_num, CLIENT_API_VERSION
        )

    def ghs_disconnect(self):
        """Disconnects from a connected mainframe.

        Returns:
            String value representing API status.
        """

        return _connection.disconnect(self._con_handle)

    def ghs_get_client_api_version(self):
        """Client's API version.

        Returns:
            Integer the API version number of this client.
        """

        return CLIENT_API_VERSION

    def ghs_get_current_access(self):
        """Current access permission to the mainframe.

        Returns:
            String value representing access permissions.
        """

        return _connection.get_current_access(self._con_handle)
