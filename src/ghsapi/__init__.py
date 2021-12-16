"""GEN DAQ API - Python.

The GEN DAQ API can be used to control the HBM GEN Series tethered
mainframes without using Perception.

Package Contents:
    Connections: Connection related API functions.
    Acquisition control: Acquisition control related API functions.
"""

from . import acquisition_api as _acquisition
from . import connection_api as _connection
from . import mainframe_api as _mainframe
from . import manage_recordings_api as _manage_recordings
from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSReturnValue,
    GHSSyncStatus,
    GHSUserMode,
)

CLIENT_API_VERSION = 4


class GHS:
    """GEN DAQ API object.

    Attributes:
        _con_handle: An unique identifier per mainframe connection.
    """

    def __init__(self):
        self._con_handle = ConnectionHandler()

    # Connection related API functions.
    def ghs_connect(self, ip_address: int, port_num: int) -> str:
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

    def ghs_disconnect(self) -> str:
        """Disconnects from a connected mainframe.

        Results in error when the handle is not valid and / or
        mainframe is not connected.

        Returns:
            String value representing API status.
        """

        return _connection.disconnect(self._con_handle)

    def ghs_get_client_api_version(self) -> int:
        """Client's API version.

        This function can be useful when ghs_connect() returns
        GHSReturnValue_APIMismatch.

        Returns:
            Integer the API version number of this client.
        """

        return CLIENT_API_VERSION

    def ghs_get_current_access(self) -> str:
        """Current access permission to the mainframe.

        The current access permissions might change at any time.
        For example, when Perception connects concurrently to the same
        mainframe, write access is dropped for the connected GEN DAQ
        API client. If a concurrently connected Perception disconnects,
        write access is granted to the connected GEN DAQ API client.
        API functions that require write access will return
        WriteAccessBlocked in case this client currently has no write
        access.

        Returns:
            String value representing access permissions.
        """

        return _connection.get_current_access(self._con_handle)

    # Acquisition control related API functions.
    def ghs_start_preview(self) -> str:
        """Starts preview mode.

        The system needs to be idle before calling this function.

        Returns:
            String value representing API status.
        """

        return _acquisition.start_preview(self._con_handle)

    def ghs_stop_preview(self) -> str:
        """Stops preview mode.

        The system needs to be in preview mode before calling this
        function.

        Returns:
            String value representing API status.
        """

        return _acquisition.stop_preview(self._con_handle)

    def ghs_start_recording(self) -> str:
        """Start recording on local storage.

        The system needs to be idle before calling this function. Note
        that the connected mainframe will generate a recording name.
        This command can be executed only successfully when the local
        storage is set.

        Returns:
            String value representing API status.
        """

        return _acquisition.start_recording(self._con_handle)

    def ghs_pause_recording(self) -> str:
        """Pauses a started recording.

        The system needs to be recording before calling this function.

        Returns:
            String value representing API status.
        """

        return _acquisition.pause_recording(self._con_handle)

    def ghs_resume_recording(self) -> str:
        """Resumes a paused recording.

        The system needs to be paused before calling this function.

        Returns:
            String value representing API status.
        """

        return _acquisition.resume_recording(self._con_handle)

    def ghs_stop_recording(self) -> str:
        """Stops a started recording.

        The system needs to be recording before calling this function.

        Returns:
            String value representing API status.
        """

        return _acquisition.stop_recording(self._con_handle)

    def ghs_trigger(self) -> str:
        """Issues a trigger.

        Results in error when the trigger cannot be issued.

        Returns:
            String value representing API status.
        """

        return _acquisition.trigger(self._con_handle)

    def ghs_get_acquisition_state(self) -> tuple[str, str | None]:
        """Returns the Acquisition State of the Mainframe.

        Returns:
            Tuple with status and acquisition state of the mainframe.
        """

        return _acquisition.get_acquisition_state(self._con_handle)

    def ghs_get_acquisition_start_time(
        self,
    ) -> tuple[str, int | None, int | None, float | None]:
        """Retrieves the absolute time of the start of acquisition.

        Returns:
            Tuple with status and the absolute time of the start of
            acquisition.
        """

        return _acquisition.get_acquisition_start_time(self._con_handle)

    def ghs_get_acquisition_time(self) -> tuple[str, float | None]:
        """Retrieves the current acquisition time relative to the start
        of acquistion.

        Returns:
            Tuple with status and current acquisition time relative to
            the start of acquistion.
        """

        return _acquisition.get_acquisition_time(self._con_handle)

    # Mainframe APIs

    def ghs_identify(self, identity_flag: bool) -> str:
        """Enable or disable the identification sound of the connected
        mainframe.

        Args:
            identity_flag: Enable or disable flag.

        Returns:
            String value representing API status.
        """

        return _mainframe.identity(self._con_handle, identity_flag)

    def ghs_get_disk_space(self) -> tuple[str, float | None, float | None]:
        """Get total and available mainframe internal disk space.

        Returns:
            Tuple with status, total mainframe internal disk space in
            GB, available internal disk space in GB.
        """

        return _mainframe.get_disk_space(self._con_handle)

    def ghs_get_sync_status(self) -> tuple[str, str | None]:
        """Determine the mainframe sync status.

        Returns:
            Tuple with API status and Sync status.
        """

        return _mainframe.get_sync_status(self._con_handle)

    def ghs_get_slot_count(self) -> tuple[str, int | None]:
        """Retrieve the number of slots in the mainframe.

        Returns:
            Tuple with API status and number of slots in the mainframe.
        """

        return _mainframe.get_slot_count(self._con_handle)

    def ghs_get_user_mode(self) -> tuple[str, str | None]:
        """Retrieve the user mode.

        Returns:
            Tuple with API status and user mode.
        """

        return _mainframe.get_user_mode(self._con_handle)

    def ghs_set_user_mode(self, user_mode: str | int) -> str:
        """Set the user mode.

        The system needs to be idle before calling this function.

        Args:
            user_mode: The desired user mode.

        Returns:
            String value representing API status.
        """

        return _mainframe.set_user_mode(self._con_handle, user_mode)

    def ghs_get_mainframe_info(
        self,
    ) -> tuple[str, str | None, str | None, str | None, str | None]:
        """Determine type, name, serial number and firmware version
        information for the connected mainframe.

        The mainframeType, mainframeName, serialNumber and
        firmwareVersion parameters are UTF-8 encoded.

        Returns:
            Tuple with API status and user mode.
        """

        return _mainframe.get_mainframe_info(self._con_handle)

    # Manage recordings APIs

    def ghs_delete_all_recordings(self) -> str:
        """Deletes all recordings from local mainframe storage.

        Recordings are deleted asynchronously.

        Returns:
            String value representing request status.
        """

        return _manage_recordings.delete_all_recordings(self._con_handle)

    def ghs_delete_last_recording(self) -> str:
        """Deletes the most recent recording from local mainframe
        storage.

        Recordings are deleted asynchronously.

        Returns:
            String value representing request status.
        """

        return _manage_recordings.delete_last_recording(self._con_handle)

    def ghs_get_recording_name(self) -> tuple[str, str | None, int | None]:
        """Retrieve the recording base name and recording index of the
        last recording file.

        The recording base name parameter is UTF-8 encoded.

        Returns:
            Tuple with status, base name and index of the recording
            file.
        """

        return _manage_recordings.get_recording_name(self._con_handle)

    def ghs_get_storage_location(self) -> tuple[str, str | None]:
        """Retrieve the storage location.

        Returns:
            Tuple with status and storage location.
        """

        return _manage_recordings.get_storage_location(self._con_handle)

    def ghs_get_high_low_rate_storage_enabled(
        self, source: str | int, slot_id: str
    ) -> tuple[str, str | None, str | None]:
        """Retrieve storage enabled status of high and low rate data
        for the specified recording data source.

        Args:
            source: The recording data source to retrieve the storage
            enabled status for.
            slot_id: The slot containing the recorder to retrieve the
            storage enabled status for (e.g. 'A' for the first slot).
            This argument is only evaluated for recorder based data
            sources.

        Returns:
            Tuple with status, flag to indicate if high and low rate
            data is stored.
        """

        return _manage_recordings.get_high_low_rate_storage_enabled(
            self._con_handle, source, slot_id
        )

    def ghs_set_high_low_rate_storage_enabled(
        self,
        source: str | int,
        slot_id: str,
        high_rate_enabled: str | int,
        low_rate_enabled: str | int,
    ) -> str:
        """Enable/disable storage of high and low rate data for the
        specified recording data source.

        Args:
            source: The recording data source to retrieve the storage
            enabled status for.
            slot_id: The slot containing the recorder to retrieve the
            storage enabled status for (e.g. 'A' for the first slot).
            This argument is only evaluated for recorder based data
            sources.
            high_rate_enabled: Enable/disable storage of high rate data
            low_rate_enabled: Enable/disable storage of low rate data.

        Returns:
            String value representing request status.
        """

        return _manage_recordings.set_high_low_rate_storage_enabled(
            self._con_handle,
            source,
            slot_id,
            high_rate_enabled,
            low_rate_enabled,
        )

    def ghs_set_recording_name(
        self, recording_name: str, recording_index: int
    ) -> str:
        """Set the recording base name and recording index for the next
         recording file.

        The system needs to be idle before calling this function.
        The recording base name parameter must be UTF-8 encoded.

        Returns:
            String value representing request status.
        """

        return _manage_recordings.set_recording_name(
            self._con_handle, recording_name, recording_index
        )

    def ghs_set_storage_location(self, storage_location: str | int) -> str:
        """Set the storage location.

        The system needs to be idle before calling this function.

        Returns:
            String value representing request status.
        """

        return _manage_recordings.set_storage_location(
            self._con_handle, storage_location
        )
