Manage recordings
=================

Recording management related API functions.


.. automethod:: ghsapi.ghsapi.GHS.ghs_get_storage_location
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_storage_location
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_recording_name
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_recording_name
.. automethod:: ghsapi.ghsapi.GHS.ghs_delete_last_recording
.. automethod:: ghsapi.ghsapi.GHS.ghs_delete_all_recordings
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_high_low_rate_storage_enabled
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_high_low_rate_storage_enabled

**Accepted values:**

- **storage_location** - "Remote", "Local1", "Local2", "iSCSI1", "iSCSI2" (Mainframe should support mentioned storage location)
- **source** - "SyncChannels", "SyncRealTimeFormulas"
- **slot_id** - e.g. 'A' for the first slot
- **high_rate_enabled/low_rate_enabled** - "Enable", "Disable"