# Copyright (C) 2022 Hottinger Bruel and Kjaer Benelux B.V.
# Schutweg 15a
# 5145 NP Waalwijk
# The Netherlands
# http://www.hbm.com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
from . import manage_mainframe_settings as _manage_mainframe_settings
from . import manage_recordings_api as _manage_recordings
from . import recorder_api as _recorder
from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSDigitalOutMode,
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
            port_num: TCP port number (currently defined as 8006).

        Returns:
            Connect return status.
        """

        return _connection.connect(
            self._con_handle, ip_address, port_num, CLIENT_API_VERSION
        )

    def ghs_disconnect(self) -> str:
        """Disconnects from a connected mainframe.

        *Results in error when the handle is not valid and / or
        mainframe is not connected.*

        Returns:
            Disconnect return status.
        """

        return _connection.disconnect(self._con_handle)

    def ghs_get_client_api_version(self) -> int:
        """Client's API version.

        *This function can be useful when ghs_connect() returns
        GHSReturnValue_APIMismatch.*

        Returns:
            Version number of the client.
        """

        return CLIENT_API_VERSION

    def ghs_get_current_access(self) -> str:
        """Current access permission to the mainframe.

        *The current access permissions might change at any time.
        For example, when Perception connects concurrently to the same
        mainframe, write access is dropped for the connected GEN DAQ
        API client. If a concurrently connected Perception disconnects,
        write access is granted to the connected GEN DAQ API client.
        API functions that require write access will return
        WriteAccessBlocked in case this client currently has no write
        access.*

        Returns:
            Access permission.
        """

        return _connection.get_current_access(self._con_handle)

    # Acquisition control related API functions.
    def ghs_start_preview(self) -> str:
        """Starts preview mode.

        *The system needs to be idle before calling this function.*

        Returns:
            Start preview status.
        """

        return _acquisition.start_preview(self._con_handle)

    def ghs_stop_preview(self) -> str:
        """Stops preview mode.

        *The system needs to be in preview mode before calling this
        function.*

        Returns:
            Stop preview status.
        """

        return _acquisition.stop_preview(self._con_handle)

    def ghs_start_recording(self) -> str:
        """Start recording on local storage.

        *The system needs to be idle before calling this function. Note
        that the connected mainframe will generate a recording name.
        This command can be executed only successfully when the local
        storage is set.*

        Returns:
            Start recording status.
        """

        return _acquisition.start_recording(self._con_handle)

    def ghs_pause_recording(self) -> str:
        """Pauses a started recording.

        *The system needs to be recording before calling this function.*

        Returns:
            Pause recording status.
        """

        return _acquisition.pause_recording(self._con_handle)

    def ghs_resume_recording(self) -> str:
        """Resumes a paused recording.

        *The system needs to be paused before calling this function.*

        Returns:
            Resume recording status.
        """

        return _acquisition.resume_recording(self._con_handle)

    def ghs_stop_recording(self) -> str:
        """Stops a started recording.

        *The system needs to be recording before calling this function.*

        Returns:
            Stop recording status.
        """

        return _acquisition.stop_recording(self._con_handle)

    def ghs_trigger(self) -> str:
        """Issues a trigger.

        Results in error when the trigger cannot be issued.

        Returns:
            Trigger status.
        """

        return _acquisition.trigger(self._con_handle)

    def ghs_get_acquisition_state(self) -> tuple[str, str | None]:
        """Returns the Acquisition State of the Mainframe.

        Returns:
            Status and acquisition state of the mainframe.
        """

        return _acquisition.get_acquisition_state(self._con_handle)

    def ghs_get_acquisition_start_time(
        self,
    ) -> tuple[str, int | None, int | None, float | None]:
        """Retrieves the absolute time of the start of acquisition.

        Returns:
            Status and the absolute time of the start of
            acquisition as year, days and seconds.
        """

        return _acquisition.get_acquisition_start_time(self._con_handle)

    def ghs_get_acquisition_time(self) -> tuple[str, float | None]:
        """Retrieves the current acquisition time relative to the start
        of acquistion.

        Returns:
            Status and current acquisition time relative to
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
            Identify API status.
        """

        return _mainframe.identity(self._con_handle, identity_flag)

    def ghs_get_disk_space(self) -> tuple[str, float | None, float | None]:
        """Get total and available mainframe internal disk space.

        Returns:
            Status, total mainframe internal disk space in
            GB, available internal disk space in GB.
        """

        return _mainframe.get_disk_space(self._con_handle)

    def ghs_get_sync_status(self) -> tuple[str, str | None]:
        """Determine the mainframe sync status.

        Returns:
            API status and sync status.
        """

        return _mainframe.get_sync_status(self._con_handle)

    def ghs_get_slot_count(self) -> tuple[str, int | None]:
        """Retrieve the number of slots in the mainframe.

        Returns:
            Status and number of slots in the mainframe.
        """

        return _mainframe.get_slot_count(self._con_handle)

    def ghs_get_user_mode(self) -> tuple[str, str | None]:
        """Retrieve the user mode.

        Returns:
            API status and user mode.
        """

        return _mainframe.get_user_mode(self._con_handle)

    def ghs_set_user_mode(self, user_mode: str | int) -> str:
        """Set the user mode.

        *The system needs to be idle before calling this function.*

        Args:
            user_mode: The desired user mode.

        Returns:
            API status.
        """

        return _mainframe.set_user_mode(self._con_handle, user_mode)

    def ghs_get_mainframe_info(
        self,
    ) -> tuple[str, str | None, str | None, str | None, str | None]:
        """Determine type, name, serial number and firmware version
        information for the connected mainframe.

        *The mainframeType, mainframeName, serialNumber and
        firmwareVersion parameters are UTF-8 encoded.*

        Returns:
            API status and mainframe info as type, name, serial number
            and firmware version.
        """

        return _mainframe.get_mainframe_info(self._con_handle)

    # Manage recordings APIs

    def ghs_delete_all_recordings(self) -> str:
        """Deletes all recordings from local mainframe storage.

        *Recordings are deleted asynchronously.*

        Returns:
            API status.
        """

        return _manage_recordings.delete_all_recordings(self._con_handle)

    def ghs_delete_last_recording(self) -> str:
        """Deletes the most recent recording from local mainframe
        storage.

        *Recordings are deleted asynchronously.*

        Returns:
            API status.
        """

        return _manage_recordings.delete_last_recording(self._con_handle)

    def ghs_get_recording_name(self) -> tuple[str, str | None, int | None]:
        """Retrieve the recording base name and recording index of the
        last recording file.

        *The recording base name parameter is UTF-8 encoded.*

        Returns:
            Status, base name and index of the recording
            file.
        """

        return _manage_recordings.get_recording_name(self._con_handle)

    def ghs_get_storage_location(self) -> tuple[str, str | None]:
        """Retrieve the storage location.

        Returns:
            Status and storage location.
        """

        return _manage_recordings.get_storage_location(self._con_handle)

    def ghs_get_high_low_rate_storage_enabled(
        self, source: str | int, slot_id: str
    ) -> tuple[str, str | None, str | None]:
        """Retrieve storage enabled status of high and low rate data
        for the specified recording data source.

        Args:
            source: The recording data source
            slot_id: The slot containing the recorder

        Returns:
            Status, flag to indicate if high and low rate
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
            source: The recording data source
            slot_id: The slot containing the recorder
            high_rate_enabled: Enable/disable storage of high rate data
            low_rate_enabled: Enable/disable storage of low rate data.

        Returns:
            API status.
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

        *The system needs to be idle before calling this function.
        The recording base name parameter must be UTF-8 encoded.*

        Args:
            recording_name: The desired base name of the recording file
            recording_index: The desired index of the recording file

        Returns:
            API status.
        """

        return _manage_recordings.set_recording_name(
            self._con_handle, recording_name, recording_index
        )

    def ghs_set_storage_location(self, storage_location: str | int) -> str:
        """Set the storage location.

        *The system needs to be idle before calling this function.*

        Args:
            storage_location: The desired storage location.

        Returns:
            API status.
        """

        return _manage_recordings.set_storage_location(
            self._con_handle, storage_location
        )

    # Manage recordings APIs

    def ghs_apply_persisted_settings(self) -> str:
        """A mainframe might contain persisted settings (being applied upon
        boot). This method re-applies these settings. In Perception this
        maps on the 'Configured boot' feature.

        *The system needs to be idle before calling this function.
        This function overwrites any previously set settings and / or
        persisted settings.*

        Returns:
            API status.
        """

        return _manage_mainframe_settings.apply_persisted_settings(
            self._con_handle
        )

    def ghs_persist_current_settings(self) -> str:
        """Persists the current mainframe settings.

        *The persisted mainframe settings are applied upon a mainframe
        boot.*

        Returns:
            API status.
        """

        return _manage_mainframe_settings.persist_current_settings(
            self._con_handle
        )

    def ghs_get_current_settings(self) -> tuple[str, bytes | None, int | None]:
        """Retrieves the current mainframe settings as a blob.

        *As this blob can be of variable size, it is upon the caller to
        ensure reading the correct amount of memory.
        Memory for this blob is allocated by the API.*

        Returns:
            Status, base name and index of the recording
            file.
        """

        return _manage_mainframe_settings.get_current_settings(
            self._con_handle
        )

    def ghs_set_current_settings(self, blob: bytes, blob_size: int) -> str:
        """Persists the current mainframe settings.

        *The persisted mainframe settings are applied upon a mainframe
        boot.*

        Args:
            blob: Settings blob.
            blob_size: Size of the settings blob.

        Returns:
            API status.
        """

        return _manage_mainframe_settings.set_current_settings(
            self._con_handle, blob, blob_size
        )

    # Recorder APIs

    def ghs_get_channel_count(self, slot_id: str) -> tuple[str, int | None]:
        """Retrieve the number of channels for a recorder.

        *This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder

        Returns:
            Status and number of channels for the recorder.
        """

        return _recorder.get_channel_count(self._con_handle, slot_id)

    def ghs_get_digital_output(
        self, slot_id: str, digital_output: str | int
    ) -> tuple[str, str | None]:
        """Retrieve the Digital Output Mode for a specified Output ID in a
        recorder.

        *This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            digital_output: The output number desired.

        Returns:
            Status and digital output mode for that output.
        """

        return _recorder.get_digital_output(
            self._con_handle, slot_id, digital_output
        )

    def ghs_get_recorder_enabled(self, slot_id: str) -> tuple[str, str | None]:
        """Determine if recorder is enabled or disabled.

        *This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder

        Returns:
            API status and recorder enabled status.
        """

        return _recorder.get_recorder_enabled(self._con_handle, slot_id)

    def ghs_get_recorder_info(
        self, slot_id: str
    ) -> tuple[str, str | None, str | None, str | None, str | None]:
        """Determine type, name, serial number and firmware version
        information for a recorder.

        *The recorderType, recorderName, serialNumber and firmwareVersion
        parameters are UTF-8 encoded.*

        *This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder

        Returns:
            Status and recorder information as type, name, serial
            number and firmware version
        """

        return _recorder.get_recorder_info(self._con_handle, slot_id)

    def ghs_get_sample_rate(self, slot_id: str) -> tuple[str, float | None]:
        """Determine the sample rate for a recorder.

        *This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder

        Returns:
            Status and sample rate for a recorder.
        """

        return _recorder.get_sample_rate(self._con_handle, slot_id)

    def ghs_set_digital_output(
        self,
        slot_id: str,
        digital_output: str | int,
        digital_output_mode: str | int,
    ) -> str:
        """Set the Digital Output Mode for a specified Output ID in a
        recorder.

        *This method will only process requests from the connected client
        with the most privileges order (Privileges order: 1- Perception,
        2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            digital_output: The output number desired.
            digital_output_mode: The digital output mode to set

        Returns:
            API status.
        """

        return _recorder.set_digital_output(
            self._con_handle, slot_id, digital_output, digital_output_mode
        )

    def ghs_set_recorder_enabled(
        self,
        slot_id: str,
        enabled: str | int,
    ) -> str:
        """Enable or disable a recorder.

        *The system needs to be idle before calling this function.*

        *This method will only process requests from the connected client
        with the most privileges order (Privileges order: 1- Perception,
        2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            enabled: Set to GHS_Enable/GHS_Disable to enable/disable

        Returns:
            API status.
        """

        return _recorder.set_recorder_enabled(
            self._con_handle, slot_id, enabled
        )

    def ghs_set_sample_rate(
        self,
        slot_id: str,
        sample_rate: float,
    ) -> str:
        """Set the sample rate for a recorder.

        *The system needs to be idle before calling this function.
        This function overwrites any previously set sample rate setting for
        the specified recorder.
        If the specified sample rate is not supported by the recorder, the
        sample rate is rounded to the nearest supported sample rate.*

        *This method will only process requests from the connected client
        with the most privileges order (Privileges order: 1- Perception,
        2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            sample_rate: In samples per second.

        Returns:
            API status.
        """
        return _recorder.set_sample_rate(
            self._con_handle, slot_id, sample_rate
        )
