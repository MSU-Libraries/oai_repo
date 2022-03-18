"""
Implementation of GetRecord verb
"""
from .exceptions import OAIErrorBadArgument
from .request import OAIRequest
from .response import OAIResponse


class GetRecordRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
        OAIErrorIdDoesNotExist
        OAIErrorCannotDisseminateFormat
    """
    def __init__(self):
        super().__init__()
        self.required_args = ["identifier", "metadataPrefix"]


class GetRecordResponse(OAIResponse):
    """
    """
