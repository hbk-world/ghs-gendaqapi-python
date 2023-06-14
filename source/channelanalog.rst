Analog
=======

Analog channel related API functions.


.. automethod:: ghsapi.ghsapi.GHS.ghs_get_trigger_settings
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_trigger_settings
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_signal_coupling
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_signal_coupling
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_input_coupling
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_input_coupling
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_span_and_offset
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_span_and_offset
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_filter_type_and_frequency
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_filter_type_and_frequency
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_excitation
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_excitation
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_amplifier_mode
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_amplifier_mode
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_technical_units
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_technical_units
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_auto_range
.. automethod:: ghsapi.ghsapi.GHS.ghs_set_auto_range
.. automethod:: ghsapi.ghsapi.GHS.ghs_cmd_auto_range_now
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_channel_cal_info
.. automethod:: ghsapi.ghsapi.GHS.ghs_get_channel_physical_name

**Accepted values:**

- **slot_id** - Analog channel slot id
- **trigger_mode** - "Basic", "Dual", "Window", "DualWindow", "Sequential", "QualifierBasic", "QualifierDual"
- **direction** - "RisingEdge", "FallingEdge"
- **signal_coupling** - "GND", "DC", "AC", "DC_RMS", "AC_RMS", "DC_Frequency", "AC_Frequency", "DC_TrueRMS", "AC_TrueRMS", "DC_ExternalProbe", "AC_ExternalProbe", "Reference", "ZeroSet", "SinglePrecision", "DoublePrecision", "QuadPrecision", "Charge"
- **input_coupling** - "SingleEndedPositive", "SingleEndedNegative", "Differential", "Current", "FloatingDifferential"
- **filter_type** - "Bessel", "Butterworth", "Elliptic", "FIR", "IIR", "Wideband", "Bessel_AA", "Butterworth_AA", "SigmaDeltaWB", "SigmaDelta", "BandPass", "FIR3dB"
- **excitation_type** - "Voltage", "Voltage_Sense", "Current", "Voltage_Strobed", "Voltage_Sense_Strobed", "Current_Strobed"
- **amplifier_mode** - "Basic", "Bridge", "Icp", "ThermoCouple", "BasicSensor", "Charge", "Current4_20", "ThermoResistor"
- **auto_range_enabled** - "Disable", "Enable"