"""
Implementation of ListMetadataFormats verb
"""
from .exceptions import OAIErrorBadArgument, OAIErrorIdDoesNotExist, OAIErrorNoMetadataFormats


class ListMetadataFormatsRequest(OAIRequest):
    """
    raises:
        OAIErrorBadArgument
        OAIErrorIdDoesNotExist      # Here or Response?
        OAIErrorNoMetadataFormats   # Here or Response?
    """
    def __init__(self):
        super().__init__(__class__.__name__)
        self.allowed_args = ['identifier']


class ListMetadataFormatsResponse(OAIResponse):
    """
    """
