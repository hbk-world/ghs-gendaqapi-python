Channel
=========

Channel related API functions.


Modules
-------

.. toctree::
   :maxdepth: 1

   channelanalog
   channeltimer

Functions
---------

.. automethod:: ghsapi.ghsapi.GHS.ghs_get_channel_type
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_channel_name
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_channel_name
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_channel_storage_enabled
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_channel_storage_enabled
.. automethod:: ghsapi.ghsapi.GHS.ghs_cmd_zeroing
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_available_span_list

**Accepted values:**

- **slot_id** - e.g. 'A' for the first slot
- **enabled** - "Enable", "Disable"
- **ezeroing** - "Enable", "Disable"