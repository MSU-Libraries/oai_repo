"""
Implementation of ListIdentifiers verb
"""
from .exceptions import OAIErrorBadArgument
from .request import OAIRequest
from .response import OAIResponse


class ListIdentifiersRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
        OAIErrorBadResumptionToken
        OAIErrorCannotDisseminateFormat
        OAIErrorNoRecordsMatch
        OAIErrorNoSetHierarchy
    """
    def __init__(self):
        super().__init__()
        self.optional_args = ["from", "until", "set"]
        self.required_args = ["metadataPrefix"]
        self.exclusive_arg = "resumptionToken"


class ListIdentifiersResponse(OAIResponse):
    """
    """
