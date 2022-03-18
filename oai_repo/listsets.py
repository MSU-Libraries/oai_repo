"""
Implementation of ListSets verb
"""
from .exceptions import OAIErrorBadArgument
from .request import OAIRequest
from .response import OAIResponse


class ListSetsRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
        OAIErrorBadResumptionToken
        OAIErrorNoSetHierarchy
    """
    def __init__(self):
        super().__init__()
        self.exclusive_arg = "resumptionToken"


class ListSetsResponse(OAIResponse):
    """
    """
