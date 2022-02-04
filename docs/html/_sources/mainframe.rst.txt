Mainframe
==========

Mainframe related API functions.


.. automethod:: ghsapi.ghsapi.GHS.ghs_identify
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_disk_space
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_sync_status
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_slot_count
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_user_mode
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_user_mode
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_mainframe_info

**Accepted values:**

- **identity_flag** - "Enable", "Disable"
- **user_mode** - "Sweeps", "Continuous", "Dual"  

*Note: Storage locations needs to be set to local mainframe storage to get disk space.*