Recorder
=========

Recorder related API functions.


.. automethod:: ghsapi.ghsapi.GHS.ghs_get_recorder_info
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_recorder_enabled
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_recorder_enabled
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_channel_count
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_sample_rate
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_sample_rate
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_digital_output
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_digital_output

**Accepted values:**

- **slot_id** - e.g. 'A' for the first slot
- **enabled** - "Enable", "Disable"
- **digital_output** - "Output1", "Output2"
- **digital_output_mode** - "Low", "High", "Acquiring", "Trigger", "Alarm"