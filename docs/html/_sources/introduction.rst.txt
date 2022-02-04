Introduction
=============

Welcome to the **GEN DAQ API - Python Driver** help file.
The GEN DAQ API can be used to control the HBM GEN Series tethered mainframes without using Perception.
Perception is a Microsoft® Windows® based application used for controlling all HBM GEN Series mainframes.
These mainframes can even run unattended, in practice the GEN DAQ API will most often be used to control the mainframe.

The controlling software will take care of the following basic tasks:

* Setting the correct predefined configuration (**ghs__set_current_settings()**)
* Getting the current configuration (**ghs__get_current_settings()**)
* Control the acquisition mode state: Start Recording, Start Preview, Stop, Pause and Resume.
* Getting / Setting the data acquisition sample rate (**ghs__set_sample_rate()**, **ghs__get_sample_rate()**)
* Generating manual triggers (**ghs__trigger()**)
* Getting / Setting the general recorder settings (**ghs_get_recorder_information()**, **ghs__get_recorder_enabled()**, **ghs_get_channel_count()**, ... )
* Getting / Setting the general channel settings (**ghs_get_channel_name()**, **ghs__set_channel_name()**, **ghs_get_channel_storage_enabled()**, **ghs_set_channel_storage_enabled()**, ... )
* Getting / Setting the Sweep settings (**ghs_get_sweep_recording_mode()**, **ghs_set_sweep_recording_mode()**, **ghs_get_sweep_length()**, **ghs_set_sweep_length()**, ... )
* Getting / Setting the Continuous settings (**ghs_get_continuous_recording_mode()**, **ghs_set_continuous_recording_mode()**, **ghs_get_continuous_lead_out_time()**, **ghs_set_continuous_lead_out_time()**, ... )
* Getting / Setting the analog channel settings (**ghs__get_aplifier_mode()**, **ghs_set_aplifier_mode()**, **ghs_get_span_and_offset()**, **ghs_set_span_and_offset()**, ...)
* Getting / Setting the timer / counter channel settings (**ghs_get_timer_counter_mode()**, **ghs_set_timer_counter_mode()**, **ghs_get_timer_counter_range()**, **ghs_set_timer_counter_range()**, ... )
* Fieldbus alike data streaming (**ghs_initiate_field_bus_data_transfer()**, **ghs_stop_field_bus_data_transfer()**, **ghs_receive_field_bus_data()**, **ghs_read_next_snapshot()**, ... )

