from .ghsapi_states import GHSReturnValue, returnKey, toString


class Connection:
    def Connect(self, conHandle, ipAdress, portNum, clientApiVersion):
        returnVar = conHandle.ConnectionEstablish(ipAdress, portNum)
        if returnVar != GHSReturnValue["OK"]:
            # return ghsReturnToString(returnVar)
            return toString(returnVar, GHSReturnValue)
        connectParamDict = {"ClientAPIVersion": clientApiVersion}

        responseJSON = conHandle.SendRequestAndWaitResponse("Connect", connectParamDict)
        # print(responseJSON)
        if responseJSON[returnKey] != GHSReturnValue["OK"]:
            return toString(responseJSON[returnKey], GHSReturnValue)
        if responseJSON["ServerAPIVersion"] != clientApiVersion:
            print(f"ServerAPIVersion : {responseJSON['ServerAPIVersion']}")
            return toString(GHSReturnValue["APIMismatch"], GHSReturnValue)

        return toString(responseJSON[returnKey], GHSReturnValue)

    def Disconnect(self, conHandle):
        responseJSON = conHandle.SendRequestAndWaitResponse("Disconnect", 0)
        # if responseJSON["GHSReturnValue"] != GHSReturnValue["OK"]:
        #     return toString(responseJSON, GHSReturnValue)
        return toString(responseJSON[returnKey], GHSReturnValue)
