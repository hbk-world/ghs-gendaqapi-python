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

"""GHS API States"""

RETURN_KEY = "GHSReturnValue"

# All possible API return values
GHSReturnValue = {
    "Reserved": 0,
    "OK": 1,
    "NOK": 2,
    "EmptySlot": 3,
    "NullPtrArgument": 4,
    "InvalidSlotID": 5,
    "SystemNotIdle": 6,
    "SystemNotRecording": 7,
    "SystemNotPaused": 8,
    "InvalidSampleRate": 9,
    "InvalidHandle": 10,
    "APIMismatch": 11,
    "ConnectionFailed": 12,
    "InvalidIP": 13,
    "MainframeTimeout": 14,
    "InsufficientDiskSpace": 15,
    "CreateRecordingFailed": 16,
    "NoConnection": 17,
    "IncompatibleStorage": 18,
    "RecordingNotFound": 19,
    "SystemNotInPreview": 20,
    "AlreadyConnected": 21,
    "InvalidRecordingName": 22,
    "InvalidChannelIndex": 23,
    "InvalidUserMode": 24,
    "InvalidChannelType": 25,
    "InvalidTriggerPosition": 26,
    "InvalidSweepMode": 27,
    "NoRecordersInMainframe": 28,
    "InvalidContinuousMode": 29,
    "InvalidModeForTriggerPosition": 30,
    "Adapted": 31,
    "InvalidUTF8Character": 32,
    "DuplicateChannelName": 33,
    "InvalidDataType": 34,
    "MethodNotFound": 35,
    "InvalidJSONFormat": 36,
    "UnkownErrorMessage": 37,
    "FieldBusAlready_Enabled": 39,
    "CANBusNotFound": 46,
    "WriteAccessBlocked": 47,
    "InvalidOutputNumber": 49,
    "IncompatibleDigitalOutputMode": 50,
}

GHSAccess = {
    "ReadOnly": 0,
    "ReadWrite": 1,
}

GHSAcquisitionState = {
    "Reserved": 0,
    "Recording": 1,
    "Pause": 2,
    "SavingData": 3,
    "Idle": 4,
    "Preview": 5,
}

GHSSyncStatus = {
    "Reserved": 0,
    "NotSynced": 1,
    "Syncing": 2,
    "Synced": 3,
    "ReSyncing": 4,
    "NoSignal": 5,
    "CoarseSynced": 6,
    "NoGMR1000": 7,
    "NoOTMC100": 8,
}

GHSUserMode = {
    "Reserved": 0,
    "Sweeps": 1,
    "Continuous": 2,
    "Dual": 3,
}

GHSStorageLocation = {
    "Reserved": 0,
    "Remote": 1,
    "Local1": 2,
    "Local2": 3,
    "iSCSI1": 4,
    "iSCSI2": 5,
}

GHSSweepRecordingMode = {"Reserved": 0, "Normal": 1, "PreTrigger": 2}

GHSContinuousRecordingMode = {
    "Reserved": 0,
    "Standard": 1,
    "Circular": 2,
    "Limited": 3,
    "StopOnTrigger": 4,
}

GHSChannelType = {
    "Invalid": 0,
    "Analog": 1,
    "Event": 2,
    "TimerCounter": 3,
}

GHSAmplifierMode = {
    "None": -1,
    "Basic": 0,
    "Bridge": 1,
    "Icp": 2,
    "ThermoCouple": 3,
    "BasicSensor": 4,
    "Charge": 5,
    "Current4_20": 6,
    "ThermoResistor": 7,
}

GHSExcitationType = {
    "Voltage": 0,
    "Voltage_Sense": 1,
    "Current": 2,
    "Voltage_Strobed": 3,
    "Voltage_Sense_Strobed": 4,
    "Current_Strobed": 5,
}

GHSFilterType = {
    "Bessel": 0,
    "Butterworth": 1,
    "Elliptic": 2,
    "FIR": 3,
    "IIR": 4,
    "Wideband": 5,
    "Bessel_AA": 6,
    "Butterworth_AA": 7,
    "SigmaDeltaWB": 8,
    "SigmaDelta": 9,
    "BandPass": 10,
    "FIR3dB": 11,
}

GHSInputCoupling = {
    "SingleEndedPositive": 0,
    "SingleEndedNegative": 1,
    "Differential": 2,
    "Current": 3,
    "FloatingDifferential": 4,
}

GHSSignalCoupling = {
    "GND": 0,
    "DC": 1,
    "AC": 2,
    "DC_RMS": 3,
    "AC_RMS": 4,
    "DC_Frequency": 5,
    "AC_Frequency": 6,
    "DC_TrueRMS": 7,
    "AC_TrueRMS": 8,
    "DC_ExternalProbe": 9,
    "AC_ExternalProbe": 10,
    "Reference": 11,
    "ZeroSet": 12,
    "SinglePrecision": 13,
    "DoublePrecision": 14,
    "QuadPrecision": 15,
    "Charge": 16,
}

GHSTriggerMode = {
    "Off": 0,
    "Basic": 1,
    "Dual": 2,
    "Window": 3,
    "DualWindow": 4,
    "Sequential": 5,
    "QualifierBasic": 6,
    "QualifierDual": 7,
}

GHSDirection = {"RisingEdge": 0, "FallingEdge": 1}

GHSTimerCounterMode = {
    "RPMUniDirectional": 0,
    "RPMBiDirectional": 1,
    "RPMQuadrature": 2,
    "FrequencyUniDirectional": 3,
    "FrequencyBiDirectional": 4,
    "FrequencyQuadrature": 5,
    "CountUniDirectional": 6,
    "CountBiDirectional": 7,
    "CountQuadrature": 8,
    "AngleQuadrature": 9,
    "AngleQuadratureWithRefPos": 10,
    "AngleUniDirectional": 11,
    "AngleUniDirectionalWithRefPos": 12,
    "AngleBiDirectional": 13,
    "AngleBiDirectionalWithRefPos": 14,
}

GHSEnableDisable = {
    "Disable": 0,
    "Enable": 1,
}

GHSRecordingDataSource = {
    "SyncChannels": 0,
    "SyncRealTimeFormulas": 1,
}

GHSDigitalOutput = {
    "Output1": 0,
    "Output2": 1,
}

GHSDigitalOutMode = {
    "Low": 0,
    "High": 1,
    "Acquiring": 2,
    "Trigger": 3,
    "Alarm": 4,
}

GHSChannelType = {
    "Invalid": 0,
    "Analog": 1,
    "Event": 2,
    "TimerCounter": 3
}

def to_string(value: int, ghs_dict: dict) -> str:
    """Get status key by value from dictionary."""

    for string_val, return_val in ghs_dict.items():
        if value == return_val:
            return string_val
    if ghs_dict == "GHSChannelType":
        return "Invalid"
    return "Reserved"


def from_string(key: str, ghs_dict: dict) -> int:
    """Get status value by key from dictionary."""

    for string_val, return_val in ghs_dict.items():
        if key == string_val:
            return return_val
    return 0


# TODO: Formating down from here
def getDictEntryFromValue(value, ghsDict):
    for stringReturnVal, returnVal in ghsDict.items():
        if value == returnVal:
            return {stringReturnVal: value}


def getDictEntryFromKey(key, ghsDict):
    for stringReturnVal, returnVal in ghsDict.items():
        if key == stringReturnVal:
            return {key: returnVal}
