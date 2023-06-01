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
from . import channel_api as _channel
from . import connection_api as _connection
from . import mainframe_api as _mainframe
from . import manage_mainframe_settings as _manage_mainframe_settings
from . import manage_recordings_api as _manage_recordings
from . import recorder_api as _recorder
from .connection import ConnectionHandler
from .ghsapi_states import (
    RETURN_KEY,
    GHSChannelType,
    GHSDigitalOutMode,
    GHSDirection,
    GHSEnableDisable,
    GHSReturnValue,
    GHSSyncStatus,
    GHSTriggerMode,
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
            * GHSReturnValue - Connect return status.
        """

        return _connection.connect(
            self._con_handle, ip_address, port_num, CLIENT_API_VERSION
        )

    def ghs_disconnect(self) -> str:
        """Disconnects from a connected mainframe.

        *Results in error when the handle is not valid and / or
        mainframe is not connected.*

        Returns:
            * GHSReturnValue - Disconnect return status.
        """

        return _connection.disconnect(self._con_handle)

    def ghs_get_client_api_version(self) -> int:
        """Client's API version.

        *This function can be useful when ghs_connect() returns
        GHSReturnValue_APIMismatch.*

        Returns:
            * CLIENT_API_VERSION - Version number of the client.
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
            * GHSAccess - Access permission.
        """

        return _connection.get_current_access(self._con_handle)

    # Acquisition control related API functions.
    def ghs_start_preview(self) -> str:
        """Starts preview mode.

        *The system needs to be idle before calling this function.*

        Returns:
            * GHSReturnValue - Start preview status.
        """

        return _acquisition.start_preview(self._con_handle)

    def ghs_stop_preview(self) -> str:
        """Stops preview mode.

        *The system needs to be in preview mode before calling this
        function.*

        Returns:
            * GHSReturnValue - Stop preview status.
        """

        return _acquisition.stop_preview(self._con_handle)

    def ghs_start_recording(self) -> str:
        """Start recording on local storage.

        *The system needs to be idle before calling this function. Note
        that the connected mainframe will generate a recording name.
        This command can be executed only successfully when the local
        storage is set.*

        Returns:
            * GHSReturnValue - Start recording status.
        """

        return _acquisition.start_recording(self._con_handle)

    def ghs_pause_recording(self) -> str:
        """Pauses a started recording.

        *The system needs to be recording before calling this function.*

        Returns:
            * GHSReturnValue - Pause recording status.
        """

        return _acquisition.pause_recording(self._con_handle)

    def ghs_resume_recording(self) -> str:
        """Resumes a paused recording.

        *The system needs to be paused before calling this function.*

        Returns:
            * GHSReturnValue - Resume recording status.
        """

        return _acquisition.resume_recording(self._con_handle)

    def ghs_stop_recording(self) -> str:
        """Stops a started recording.

        *The system needs to be recording before calling this function.*

        Returns:
            * GHSReturnValue - Stop recording status.
        """

        return _acquisition.stop_recording(self._con_handle)

    def ghs_trigger(self) -> str:
        """Issues a trigger.

        Results in error when the trigger cannot be issued.

        Returns:
            * GHSReturnValue - Trigger status.
        """

        return _acquisition.trigger(self._con_handle)

    def ghs_get_acquisition_state(self) -> tuple[str, str | None]:
        """Returns the Acquisition State of the Mainframe.

        Returns:
            * GHSReturnValue - API return status
            * GHSAcquisitionState - acquisition state of the mainframe.
        """

        return _acquisition.get_acquisition_state(self._con_handle)

    def ghs_get_acquisition_start_time(
        self,
    ) -> tuple[str, int | None, int | None, float | None]:
        """Retrieves the absolute time of the start of acquisition.

        Returns:
            * GHSReturnValue - API return status
            * year - The year
            * day - The day number in the year
            * seconds -The number of seconds since midnight.
        """

        return _acquisition.get_acquisition_start_time(self._con_handle)

    def ghs_get_acquisition_time(self) -> tuple[str, float | None]:
        """Retrieves the current acquisition time relative to the start
        of acquistion.

        Returns:
            * GHSReturnValue - API return status
            * acquisition_time - The acquisition time in seconds.
        """

        return _acquisition.get_acquisition_time(self._con_handle)

    # Mainframe APIs

    def ghs_identify(self, identity_flag: bool) -> str:
        """Enable or disable the identification sound of the connected
        mainframe.

        Args:
            identity_flag: Enable or disable flag.

        Returns:
            * GHSReturnValue - Identify API status.
        """

        return _mainframe.identity(self._con_handle, identity_flag)

    def ghs_get_disk_space(self) -> tuple[str, float | None, float | None]:
        """Get total and available mainframe internal disk space.

        Returns:
            * GHSReturnValue - API return status
            * total - Total mainframe internal disk space in GB
            * available - Available internal disk space in GB
        """

        return _mainframe.get_disk_space(self._con_handle)

    def ghs_get_sync_status(self) -> tuple[str, str | None]:
        """Determine the mainframe sync status.

        Returns:
            * GHSReturnValue - API return status
            * GHSSyncStatus - Sync status
        """

        return _mainframe.get_sync_status(self._con_handle)

    def ghs_get_slot_count(self) -> tuple[str, int | None]:
        """Retrieve the number of slots in the mainframe.

        Returns:
            * GHSReturnValue - API return status
            * slot_count - The number of slots in the mainframe
        """

        return _mainframe.get_slot_count(self._con_handle)

    def ghs_get_user_mode(self) -> tuple[str, str | None]:
        """Retrieve the user mode.

        Returns:
            * GHSReturnValue - API return status
            * GHSUserMode - The user mode
        """

        return _mainframe.get_user_mode(self._con_handle)

    def ghs_set_user_mode(self, user_mode: str | int) -> str:
        """Set the user mode.

        *The system needs to be idle before calling this function.*

        Args:
            user_mode: The desired user mode.

        Returns:
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
            * mainframe_type - The type of the mainframe
            * mainframe_name - The name of the mainframe
            * serial_number - The serial number of the mainframe
            * firmware_version - The firmware version of the mainframe
        """

        return _mainframe.get_mainframe_info(self._con_handle)

    # Manage recordings APIs

    def ghs_delete_all_recordings(self) -> str:
        """Deletes all recordings from local mainframe storage.

        *Recordings are deleted asynchronously.*

        Returns:
            * GHSReturnValue - API return status
        """

        return _manage_recordings.delete_all_recordings(self._con_handle)

    def ghs_delete_last_recording(self) -> str:
        """Deletes the most recent recording from local mainframe
        storage.

        *Recordings are deleted asynchronously.*

        Returns:
            * GHSReturnValue - API return status
        """

        return _manage_recordings.delete_last_recording(self._con_handle)

    def ghs_get_recording_name(self) -> tuple[str, str | None, int | None]:
        """Retrieve the recording base name and recording index of the
        last recording file.

        *The recording base name parameter is UTF-8 encoded.*

        Returns:
            * GHSReturnValue - API return status
            * recording_base_name - The base name of the recording file
            * recording_index - The index of the recording file
        """

        return _manage_recordings.get_recording_name(self._con_handle)

    def ghs_get_storage_location(self) -> tuple[str, str | None]:
        """Retrieve the storage location.

        Returns:
            * GHSReturnValue - API return status
            * GHSStorageLocation - The storage location
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
            * GHSReturnValue - API return status
            * GHSEnableDisable - Flag to indicate if high rate data is stored
            * GHSEnableDisable - Flag to indicate if low rate data is stored
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
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
            * blob - Pointer to the settings blob
            * blob_size - Size of the settings blob
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
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
            * channel_count - The number of channels for the recorder
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
            * GHSReturnValue - API return status
            * GHSDigitalOutMode - The digital output mode for that output
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
            * GHSReturnValue - API return status
            * GHSEnableDisable - The recorder enabled status
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
            * GHSReturnValue - API return status
            * recorder_type - The type of the recorder
            * recorder_name - The name of the recorder
            * serial_number - The serial number of the recorder
            * firmware_version - The firmware version of the recorder
        """

        return _recorder.get_recorder_info(self._con_handle, slot_id)

    def ghs_get_sample_rate(self, slot_id: str) -> tuple[str, float | None]:
        """Determine the sample rate for a recorder.

        *This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder

        Returns:
            * GHSReturnValue - API return status
            * sample_rate - in samples per second
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
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
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
            * GHSReturnValue - API return status
        """
        return _recorder.set_sample_rate(
            self._con_handle, slot_id, sample_rate
        )

    # Channel APIs

    ## Functions

    def ghs_get_channel_type(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, int | None]:
        """Determine the type of a channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSChannelType - Type of the channel
        """

        return _channel.get_channel_type(
            self._con_handle, slot_id, channel_index
        )

    def ghs_get_channel_name(
        self,
        slot_id: str,
        channel_index: int,
        channel_type: str | int,
    ) -> tuple[str, int | None]:
        """Determine the name of a channel.

        *The channel name is UTF-8 encoded*

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The one-based index of the specified channel type
            channel_type: The specific channel type

        Returns:
            * GHSReturnValue - API return values
            * channel_name - The name of the channel
        """

        return _channel.get_channel_name(
            self._con_handle, slot_id, channel_index, channel_type
        )

    def ghs_set_channel_name(
        self,
        slot_id: str,
        channel_index: int,
        channel_type: str | int,
        channel_name: str
    ) -> str:
        """Set the name for a channel.

        *The channel name is UTF-8 encoded*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The one-based index of the specified channel type
            channel_type: The specific channel type
            channel_name: The name of the channel

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_channel_name(
            self._con_handle, slot_id, channel_index, channel_type, channel_name
        )

    def ghs_get_channel_storage_enabled(
        self,
        slot_id: str,
        channel_index: int,
        channel_type: str | int,
    ) -> tuple[str, str | None]:
        """Determine if storage is enabled or disabled for a channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The one-based index of the channel
            channel_type: The specific channel type

        Returns:
            * GHSReturnValue - API return values
            * GHSEnableDisable - The storage enabled status for the channel
        """

        return _channel.get_channel_storage_enabled(
            self._con_handle, slot_id, channel_index, channel_type
        )

    def ghs_set_channel_storage_enabled(
        self,
        slot_id: str,
        channel_index: int,
        channel_type: str | int,
        enabled: str | int,
    ) -> str:
        """Enable or disable storage for a channel.

        *The system needs to be idle before calling this function.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The one-based index of the channel
            channel_type: The specific channel type
            enabled: The desired storage enabled status for the channel

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_channel_storage_enabled(
            self._con_handle, slot_id, channel_index, channel_type, enabled
        )

    def ghs_cmd_zeroing(
        self,
        slot_id: str,
        channel_index: int,
        channel_type: str | int,
        ezeroing: str | int
    ) -> str:
        """Perform zeroing in a channel.

        *The system needs to be idle before calling this function.*

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The one-based index of the channel
            channel_type: The specific channel type
            ezeroing: Zero / Unzero the specific channel

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.cmd_zeroing(
            self._con_handle, slot_id, channel_index, channel_type, ezeroing
        )

    ## Analog Module

    def ghs_get_trigger_settings(
        self, slot_id: str, channel_index: int
    ) -> tuple[
        str, str | None, float | None, float | None, float | None, str | None
    ]:
        """Determine the trigger settings for an analog channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSTriggerMode - Trigger Mode
            * primary_level - The primary trigger level
            * secondary_level - The secondary trigger level
            * hysteresis - The trigger hysteresis
            * direction - The trigger direction
        """

        return _channel.get_trigger_settings(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_trigger_settings(
        self,
        slot_id: str,
        channel_index: int,
        trigger_mode: str | int,
        primary_level: float,
        secondary_level: float,
        hysteresis: float,
        direction: str | int,
    ) -> str:
        """Set the trigger settings for an analog channel.

        *The system needs to be idle before calling this function.*

        *This function overwrites any previously set trigger settings
        for the specified recorder.*

        *If the specified trigger mode or value is not supported by the
        recorder, the trigger mode remains unchanged or the value is
        rounded to the nearest supported value.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            trigger_mode: Trigger Mode. Default is Basic
            primary_level: The desired primary trigger level
            secondary_level: The desired secondary trigger level
            hysteresis: The desired trigger hysteresis
            direction: The desired trigger direction

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_trigger_settings(
            self._con_handle,
            slot_id,
            channel_index,
            trigger_mode,
            primary_level,
            secondary_level,
            hysteresis,
            direction,
        )

    def ghs_get_signal_coupling(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None]:
        """Determine the signal coupling for an analog channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSSignalCoupling - The signal coupling
        """

        return _channel.get_signal_coupling(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_signal_coupling(
        self,
        slot_id: str,
        channel_index: int,
        signal_coupling: str | int,
    ) -> str:
        """Set the signal coupling for an analog channel.

        *If the specified signal coupling mode is not supported by the
        recorder, the signal coupling mode remains unchanged.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            signal_coupling: The desired signal coupling.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_signal_coupling(
            self._con_handle,
            slot_id,
            channel_index,
            signal_coupling,
        )

    def ghs_get_input_coupling(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None]:
        """Determine the input coupling for an analog channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSInputCoupling - The input coupling
        """

        return _channel.get_input_coupling(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_input_coupling(
        self,
        slot_id: str,
        channel_index: int,
        input_coupling: str | int,
    ) -> str:
        """Set the input coupling for an analog channel.

        *If the specified input coupling mode is not supported by the
        recorder, the input coupling mode remains unchanged.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            input_coupling: The desired input coupling.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_input_coupling(
            self._con_handle,
            slot_id,
            channel_index,
            input_coupling,
        )

    def ghs_get_span_and_offset(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, float | None, float | None]:
        """Determine the span and offset for an analog channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * span - The span in user units
            * offset - The offset in user units
        """

        return _channel.get_span_and_offset(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_span_and_offset(
        self,
        slot_id: str,
        channel_index: int,
        span: float,
        offset: float,
    ) -> str:
        """Set Span and offset for analog channels.

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            span: The span in user units. The value is adapted to available options.
            offset: The offset in user units. The value is adapted to available options.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_span_and_offset(
            self._con_handle,
            slot_id,
            channel_index,
            span,
            offset,
        )

    def ghs_get_filter_type_and_frequency(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None, float | None]:
        """Determine the filter type and frequency for an analog channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSFilterType - The filter type
            * frequency - The filter frequency in Hz
        """

        return _channel.get_filter_type_and_frequency(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_filter_type_and_frequency(
        self,
        slot_id: str,
        channel_index: int,
        filter_type: str | int,
        frequency: float,
    ) -> str:
        """Set the filter type and frequency for an analog channel.

        *This function overwrites any previously set filter settings
        for the specified recorder.*

        *If a specified filter type or value is not supported by the
        recorder, the filter type remains the same or the value is rounded to
        a supported vale.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            filter_type: The filter type. Default is Bessel.
            frequency: The filter frequency in Hz.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_filter_type_and_frequency(
            self._con_handle,
            slot_id,
            channel_index,
            filter_type,
            frequency,
        )

    def ghs_get_excitation(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None, float | None]:
        """Determine the excitation type and value for an analog channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSExcitationType - The excitation type
            * excitation_value - The excitation value in user units (voltage or current).
        """

        return _channel.get_excitation(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_excitation(
        self,
        slot_id: str,
        channel_index: int,
        excitation_type: str | int,
        excitation_value: float,
    ) -> str:
        """Set the excitation type and value for an analog channel.

        *The system needs to be idle before calling this function.*

        *If the specified excitation type or value is not supported by the
        recorder, the excitation type remains unchanged or the value is
        rounded to the nearest supported value.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            excitation_type: The desired excitation type. Default is Voltage.
            excitation_value: The desired excitation value in user units (voltage or current).

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_excitation(
            self._con_handle,
            slot_id,
            channel_index,
            excitation_type,
            excitation_value,
        )

    def ghs_get_amplifier_mode(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None]:
        """Determine the amplifier mode for an analog channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSAmplifierMode - The amplifier mode
        """

        return _channel.get_amplifier_mode(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_amplifier_mode(
        self,
        slot_id: str,
        channel_index: int,
        amplifier_mode: str | int,
    ) -> str:
        """Set the amplifier mode for an analog channel.

        *The system needs to be idle before calling this function.*

        *If the specified amplifier mode is not supported by the recorder, the
        amplifier mode remains unchanged.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            amplifier_mode: The desired amplifier mode

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_amplifier_mode(
            self._con_handle,
            slot_id,
            channel_index,
            amplifier_mode,
        )

    def ghs_get_technical_units(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None, float | None, float | None]:
        """Determine the technical units, unit multiplier and unit offset for
        an analog channel.

        *The units parameter is UTF-8 encoded.*

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * units - The technical units (e.g. 'V' for Volt or 'Hz' for Hertz).
            * multiplier - The technical units multiplier value.
            * offset - The technical units offset value.
        """

        return _channel.get_technical_units(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_technical_units(
        self,
        slot_id: str,
        channel_index: int,
        units: str,
        multiplier: float,
        offset: float,
    ) -> str:
        """Set the technical units, unit multiplier and unit offset for an
        analog channel.

        *The units parameter must be UTF-8 encoded.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            units: The desired technical units (e.g. 'V' for Volt or 'Hz' for Hertz).
            multiplier: The desired technical units multiplier value.
            offset: The desired technical units offset value.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_technical_units(
            self._con_handle,
            slot_id,
            channel_index,
            units,
            multiplier,
            offset,
        )

    def ghs_get_auto_range(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None, float | None]:
        """Determine the auto range enable and time settings.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSEnableDisable - The auto range enabled setting.
            * auto_range_time - The time for auto range in seconds.
        """

        return _channel.get_auto_range(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_auto_range(
        self,
        slot_id: str,
        channel_index: int,
        auto_range_enabled: str | int,
        auto_range_time: float,
    ) -> str:
        """Set Auto range settings for analog channels.

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            auto_range_enabled: The auto range enabled setting. The value is adapted to available options.
            auto_range_time: The time for auto range in seconds. The value is adapted to available options.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_auto_range(
            self._con_handle,
            slot_id,
            channel_index,
            auto_range_enabled,
            auto_range_time,
        )

    def ghs_cmd_auto_range_now(
        self,
        slot_id: str,
        channel_index: int,
        auto_range_time: float,
    ) -> str:
        """Command a single shot for auto range.

        *The system needs to be acquiring for this function to have any
        effect.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            auto_range_time: The time for auto range in seconds. The value is adapted to available options.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.cmd_auto_range_now(
            self._con_handle,
            slot_id,
            channel_index,
            auto_range_time,
        )

    def ghs_get_channel_cal_info(
        self, slot_id: str, channel_index: int
    ) -> tuple[
        str,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
        str | None,
    ]:
        """Retrieve calibration information for an analog channel.

        *The calibrationDateTime, verificationDateTime,
        powerVerificationDateTime, calibrationLab, verificationLab and
        powerVerificationLab parameters are UTF-8 encoded.*

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * calibration_date_time - The date and time this analog channel has been calibrated.
            * verification_date_time - The date and time the calibration for this analog channel has been verified.
            * power_verification_date_time - The date and time the power calibration for this analog channel has been verified (if applicable).
            * calibration_lab - The laboratory that conducted the calibration for this analog channel.
            * verification_lab - The laboratory that verified the calibration for this analog channel.
            * power_verification_lab - The laboratory that verified the power calibration for this analog channel (if applicable).
        """

        return _channel.get_channel_cal_info(
            self._con_handle, slot_id, channel_index
        )

    ## Timer/Counter Module

    def ghs_get_timer_counter_gate_time(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, float | None]:
        """Determine the gate time for a timer/counter channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * gate_time - The gate time in seconds
        """

        return _channel.get_timer_counter_gate_time(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_timer_counter_gate_time(
        self,
        slot_id: str,
        channel_index: int,
        gate_time: float,
    ) -> str:
        """Determine the gate time for a timer/counter channel.

        The system needs to be idle before calling this function.

        If the specified timer/counter gate time is not supported by the
        recorder, the timer/counter gate time is rounded to the nearest
        supported gate time.

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            gate_time: The desired gate time in seconds.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_timer_counter_gate_time(
            self._con_handle,
            slot_id,
            channel_index,
            gate_time,
        )

    def ghs_get_timer_counter_mode(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, str | None]:
        """Determine the mode for a timer/counter channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * GHSTimerCounterMode - The timer/counter mode
        """

        return _channel.get_timer_counter_mode(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_timer_counter_mode(
        self,
        slot_id: str,
        channel_index: int,
        mode: str | int,
    ) -> str:
        """Set the mode for a timer/counter channel.

        *The system needs to be idle before calling this function.*

        *If the specified timer/counter mode is not supported by the recorder, the
        timer/counter mode remains unchanged.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            mode: The desired timer/counter mode. Default is RPMUniDirectional.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_timer_counter_mode(
            self._con_handle,
            slot_id,
            channel_index,
            mode,
        )

    def ghs_get_timer_counter_range(
        self, slot_id: str, channel_index: int
    ) -> tuple[str, float | None, float | None]:
        """Determine the range for a timer/counter channel.

        *Read - This method can be called by multiple connected clients at same
        time.*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel

        Returns:
            * GHSReturnValue - API return values
            * lower_value - The lower range value.
            * upper_value - The upper range value.
        """

        return _channel.get_timer_counter_range(
            self._con_handle, slot_id, channel_index
        )

    def ghs_set_timer_counter_range(
        self,
        slot_id: str,
        channel_index: int,
        lower_value: float,
        upper_value: float,
    ) -> str:
        """Set the range for a timer/counter channel.

        *The system needs to be idle before calling this function.*

        *If the specified timer/counter range is illegal (i.e. upperValue <
        lowerValue), the timer/counter range values are corrected to the
        nearest possible values.*

        *ReadWrite - This method will only process requests from the
        connected client with the most privileges order (Privileges
        order: 1- Perception, 2- GenDaq, 3- Other)*

        Args:
            slot_id: The slot containing the recorder
            channel_index: The zero-based index of the channel
            lower_value: The desired lower range value.
            upper_value: The desired upper range value.

        Returns:
            * GHSReturnValue - API return values
        """

        return _channel.set_timer_counter_range(
            self._con_handle,
            slot_id,
            channel_index,
            lower_value,
            upper_value,
        )
