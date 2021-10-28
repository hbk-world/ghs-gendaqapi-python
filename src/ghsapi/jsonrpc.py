import json
from collections import OrderedDict

from .ghsapi_states import GHSReturnValue, returnKey


def createJSONrpc(requestId, methodName, methodParam):
    if methodParam != 0:
        jsonObj = OrderedDict(
            [
                ("jsonrpc", "2.0"),
                ("method", methodName),
                ("params", methodParam),
                ("id", requestId),
            ]
        )
    else:
        jsonObj = OrderedDict(
            [("jsonrpc", "2.0"), ("method", methodName), ("id", requestId)]
        )
    requestJSON = json.dumps(jsonObj, separators=(",", ":")) + "\0"
    return requestJSON.encode("utf-8")


def parseJSONrpc(requestId, responseJSON):
    parsedJSON = json.loads(responseJSON[:-1])
    returnVar = checkJSONrpcError(requestId, parsedJSON)
    if returnVar != GHSReturnValue["OK"]:
        return {returnKey: returnVar}
    if isinstance(parsedJSON["result"], int):
        return {returnKey: parsedJSON["result"]}
    return parsedJSON["result"]


def checkJSONrpcError(requestId, responseDict):
    if int(responseDict["id"]) != requestId:
        return GHSReturnValue["NOK"]
    if responseDict["id"] == "null":
        # needs other error handling
        return GHSReturnValue["NOK"]
    else:
        return GHSReturnValue["OK"]
