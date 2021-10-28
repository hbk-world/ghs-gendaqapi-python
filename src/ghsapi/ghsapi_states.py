returnKey = 'GHSReturnValue'

GHSReturnValue = {
        'Reserved' : 0,
        'OK' : 1,
        'NOK' : 2,
        'NullPtrArgument' : 4,
        'SystemNotRecording' : 7,
        'SystemNotPaused' : 8,
        'APIMismatch' : 11,
        'ConnectionFailed' : 12,
        'MainframeTimeout' : 14,
        'NoConnection' : 17,
        'IncompatibleStorage' : 18,
        'SystemNotInPreview' : 20,
        'Adapted' : 31,
        'InvalidDataType' : 34,
        'FieldBusAlready_Enabled' : 39
}

GHSAcquisitionState = {
        'Reserved' : 0,
        'Recording' : 1,
        'Pause' : 2,
        'SavingData' : 3,
        'Idle' : 4,
        'Preview' : 5
}

GHSSyncStatus = {
        'Reserved' : 0,
        'NotSynced' : 1,
        'Syncing' : 2,
        'Synced' : 3,
        'ReSyncing' : 4,
        'NoSignal' : 5,
        'CoarseSynced' : 6,
        'NoGMR1000' : 7,
        'NoOTMC100' : 8
}

GHSUserMode = {
        'Reserved' : 0,
        'Sweeps' : 1,
        'Continuous' : 2,
        'Dual' : 3,
}

GHSStorageLocation = {
        'Reserved' : 0,
        'Remote' : 1,
        'Local1' : 2,
        'Local2' : 3,
        'iSCSI1' : 4,
        'iSCSI2' : 5,
}

GHSSweepRecordingMode = {
        'Reserved' : 0,
        'Normal' : 1,
        'PreTrigger' : 2
}

GHSContinuousRecordingMode = {
        'Reserved' : 0,
        'Standard' : 1,
        'Circular' : 2,
        'Limited' : 3,
        'StopOnTrigger' : 4
}

GHSChannelType = {
        'Invalid' : 0,
        'Analog' : 1,
        'Event' : 2,
        'TimerCounter' : 3
}

GHSAmplifierMode = {
    'None' : -1,
    'Basic' : 0,
    'Bridge' : 1,
    'Icp' : 2,
    'ThermoCouple' : 3,
    'BasicSensor' : 4,
    'Charge' : 5,
    'Current4_20' : 6,
    'ThermoResistor' : 7
}

GHSExcitationType = {
    'Voltage' : 0,
    'Voltage_Sense' : 1,
    'Current' : 2,
    'Voltage_Strobed' : 3,
    'Voltage_Sense_Strobed' : 4,
    'Current_Strobed' : 5
}

GHSFilterType = {
    'Bessel' : 0,
    'Butterworth' : 1,
    'Elliptic' : 2,
    'FIR': 3,
    'IIR' : 4,
    'Wideband' : 5,
    'Bessel_AA' : 6,
    'Butterworth_AA' : 7,
    'SigmaDeltaWB' : 8,
    'SigmaDelta' : 9,
    'BandPass' : 10,
    'FIR3dB' : 11
}

GHSInputCoupling = {
    'SingleEndedPositive' : 0,
    'SingleEndedNegative' : 1,
    'Differential' : 2,
    'Current' : 3,
    'FloatingDifferential' : 4,
}

GHSSignalCoupling = {
    'GND' : 0,
    'DC' : 1,
    'AC' : 2,
    'DC_RMS' : 3,
    'AC_RMS' : 4,
    'DC_Frequency' : 5,
    'AC_Frequency' : 6,
    'DC_TrueRMS' : 7,
    'AC_TrueRMS' : 8,
    'DC_ExternalProbe' : 9,
    'AC_ExternalProbe' : 10,
    'Reference' : 11,
    'ZeroSet' : 12,
    'SinglePrecision' : 13,
    'DoublePrecision' : 14,
    'QuadPrecision' : 15,
    'Charge' : 16
}

GHSTriggerMode = {
    'Off' : 0,
    'Basic' : 1,
    'Dual' : 2,
    'Window' : 3,
    'DualWindow' : 4,
    'Sequential' : 5,
    'QualifierBasic' : 6,
    'QualifierDual' : 7
}

GHSDirection = {
    'RisingEdge' : 0,
    'FallingEdge' : 1
}

GHSTimerCounterMode = {
    'RPMUniDirectional' : 0,
    'RPMBiDirectional' : 1,
    'RPMQuadrature' : 2,
    'FrequencyUniDirectional' : 3,
    'FrequencyBiDirectional' : 4,
    'FrequencyQuadrature' : 5,
    'CountUniDirectional' : 6,
    'CountBiDirectional' : 7,
    'CountQuadrature' : 8,
    'AngleQuadrature' : 9,
    'AngleQuadratureWithRefPos' : 10,
    'AngleUniDirectional' : 11,
    'AngleUniDirectionalWithRefPos' : 12,
    'AngleBiDirectional' : 13,
    'AngleBiDirectionalWithRefPos' : 14,
}

def toString(value, ghsDict):
    for stringReturnVal, returnVal in ghsDict.items():
        if value == returnVal:
            return stringReturnVal


def fromString(key, ghsDict):
    for stringReturnVal, returnVal in ghsDict.items():
        if key == stringReturnVal:
            return returnVal

def getDictEntryFromValue(value, ghsDict):
    for stringReturnVal, returnVal in ghsDict.items():
        if value == returnVal:
            return {stringReturnVal:value}

def getDictEntryFromKey(key, ghsDict):
    for stringReturnVal, returnVal in ghsDict.items():
        if key == stringReturnVal:
            return {key:returnVal}
