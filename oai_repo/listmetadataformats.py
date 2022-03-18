"""
Implementation of ListMetadataFormats verb
"""
from .exceptions import OAIErrorBadArgument, OAIErrorIdDoesNotExist, OAIErrorNoMetadataFormats
from .request import OAIRequest
from .response import OAIResponse


class ListMetadataFormatsRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
        OAIErrorIdDoesNotExist      # Here or Response?
        OAIErrorNoMetadataFormats   # Here or Response?
    """
    def __init__(self):
        super().__init__()
        self.optional_args = ['identifier']


class ListMetadataFormatsResponse(OAIResponse):
    """
    """
